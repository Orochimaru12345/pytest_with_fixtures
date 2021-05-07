import time

import docker
import json
import os
import pytest
import requests
import uuid

DOCKER_TIMEOUT = 10  # sec
APP_TIMEOUT = 5  # sec


class App(object):
    def __init__(self):
        self.app_host = os.getenv('TEST_APP_HOST') if os.getenv('TEST_APP_HOST') else '127.0.0.1'
        self.app_port = os.getenv('TEST_APP_PORT') if os.getenv('TEST_APP_PORT') else '5000'
        self.base_url = f'http://{self.app_host}:{self.app_port}'

    @staticmethod
    def _handle_connection_error(url, e):
        assert 'Ok' == 'Error', (
            '\n'
            'Service {url} is down or not reachable\n'
            'Error: {err}'.format(
                url=url,
                err=e
            )
        )

    def _req(self, method, url, **kwargs):
        for i in range(APP_TIMEOUT):
            try:
                r = requests.__dict__[method](url, **kwargs)
                return r
            except requests.exceptions.ConnectionError as e:
                if i < APP_TIMEOUT - 1:
                    time.sleep(1)
                else:
                    self._handle_connection_error(self.base_url, e)

    # Show list of uploaded templates
    def list_templates(self) -> requests.Response:
        url = self.base_url + '/api/v1/templates'

        return self._req(method='get', url=url)

    # Delete a template by its id.
    def delete_template(self, tmpl_id: str) -> requests.Response:
        url = self.base_url + '/api/v1/templates/{tmpl_id}'.format(tmpl_id=tmpl_id)

        return self._req(method='delete', url=url)

    # Upload a template to application.
    def upload_template(self, path_to_local_file: str, tmpl_id: str = "#NO") -> requests.Response:
        url = self.base_url + '/api/v1/templates'

        files = {
            'file': (path_to_local_file.split("/")[-1], open(path_to_local_file, 'rb'), 'Form-Data')
        }
        data = {}
        if tmpl_id != "#NO":
            data['data'] = json.dumps({"tmpl_id": tmpl_id})

        return self._req(method='post', url=url, data=data, files=files)

    # Install a template - HAS UNKNOWN EFFECT
    def install_template(self, tmpl_id) -> requests.Response:
        url = self.base_url + f'/api/v1/templates/{tmpl_id}/install'

        return self._req(method='post', url=url)


class DockerContainer(object):
    def __init__(self):
        self.name = uuid.uuid4().__str__()

    # noinspection PyMethodMayBeStatic
    def start(self):
        client = docker.from_env()

        # stop app
        for container in client.containers.list():
            if 'test_app:latest' in container.image.attrs['RepoTags']:
                container.stop()

        # start app
        client.containers.run(
            "test_app:latest",
            name=self.name,
            detach=True,
            ports={'5000/tcp': '5000'},
            remove=True,
            auto_remove=True
        )

        # wait for app
        for _ in range(DOCKER_TIMEOUT):
            for container in client.containers.list():
                if 'test_app:latest' in container.image.attrs['RepoTags']:
                    return

            time.sleep(1)

    # noinspection PyMethodMayBeStatic
    def stop(self):
        client = docker.from_env()

        # stop app
        for container in client.containers.list():
            if 'test_app:latest' in container.image.attrs['RepoTags']:
                try:
                    container.stop()
                    container.remove(v=True)
                except Exception as e:
                    print(e.__str__() + '\n', file=open('log.txt', mode='a'))


@pytest.fixture(scope='class')
def docker_container():
    d = DockerContainer()
    d.start()
    yield d

    d.stop()


@pytest.fixture(scope='class')  # function, class, session, module
def app():
    # run before any test functions in the scope
    # print('fixture: [#app] [#before]')
    yield App()

    # everything after the yield happens after tests in the scope
    # print('fixture: [#app] [#after]')

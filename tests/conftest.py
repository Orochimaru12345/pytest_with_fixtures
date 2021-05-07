import json
import os
import pytest
import requests


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

    # Show list of uploaded templates
    def list_templates(self) -> requests.Response:
        url = self.base_url + '/api/v1/templates'

        try:
            r = requests.get(url)
            return r
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(url, e)

    # Delete a template by its id.
    def delete_template(self, tmpl_id: str) -> requests.Response:
        url = self.base_url + '/api/v1/templates/{tmpl_id}'.format(tmpl_id=tmpl_id)

        try:
            r = requests.delete(url)
            return r
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(url, e)

    # Upload a template to application.
    def upload_template(self, path_to_local_file: str, tmpl_id: str = "#NO") -> requests.Response:
        url = self.base_url + '/api/v1/templates'

        files = {
            'file': (path_to_local_file.split("/")[-1], open(path_to_local_file, 'rb'), 'Form-Data')
        }
        data = {}
        if tmpl_id != "#NO":
            data['data'] = json.dumps({"tmpl_id": tmpl_id})

        try:
            r = requests.post(url, files=files, data=data)
            return r
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(url, e)

    # Install a template - HAS UNKNOWN EFFECT
    def install_template(self, tmpl_id) -> requests.Response:
        url = self.base_url + f'/api/v1/templates/{tmpl_id}/install'

        try:
            r = requests.post(url)
            return r
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(url, e)


class Docker(object):
    def __init__(self):
        pass


@pytest.fixture(scope='session')  # function, class, session, module
def app():
    # run before any test functions in the scope
    # print('fixture: [#app] [#before]')
    yield App()

    # everything after the yield happens after tests in the scope
    # print('fixture: [#app] [#after]')


@pytest.fixture(scope='class')
def docker():
    # print('fixture: [#docker] [#before]')
    yield Docker()

    # print('fixture: [#docker] [#after]')

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

    # Try delete a template by its id.
    def delete_template(self, tmpl_id: str) -> requests.Response:
        url = self.base_url + '/api/v1/templates/{tmpl_id}'.format(tmpl_id=tmpl_id)

        try:
            r = requests.delete(url)
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

import json
import requests

APPLICATION_JSON = 'application/json'


class Assertions(object):
    @staticmethod
    def _add_msg(description, msg):
        if msg != '':
            description = '\n' + msg + '.\n' + description
        return description

    @staticmethod
    def assert_response_status_code(r: requests.Response, code=200, msg=''):
        result = (r.status_code == code)
        description = (
            'Actual response code from {url} is {actual_code}.\n'
            'Expected {code}'
        ).format(
            url=r.url,
            actual_code=r.status_code,
            code=code
        )
        description = Assertions._add_msg(description, msg)

        assert result, description

    @staticmethod
    def assert_response_is_json(r: requests.Response, msg=''):
        content_type = r.headers.get("Content-Type")
        description = (
            'Expected header "Content-Type"'
            ' of the response from {url}'
            ' must be "{app_json}".\n'
            'But it is actually "{content_type}"\n'
            'First 500 characters of response:\n'
            '{data}'
        ).format(
            url=r.url,
            app_json=APPLICATION_JSON,
            content_type=content_type,
            data=r.text[0:500]
        )
        result = (content_type == APPLICATION_JSON)
        description = Assertions._add_msg(description, msg)

        assert result, description

        try:
            json.loads(r.text)
        except json.JSONDecodeError as e:
            description = (
                'Content of the response from {url} must be a valid JSON.\n'
                'But it is not.\n'
                'First 500 characters of response:\n'
                '{data}'
            ).format(
                url=r.url,
                app_json=APPLICATION_JSON,
                data=r.text[0:500]
            )
            assert False, description

    @staticmethod
    def assert_response_data_has_key(r: requests.Response, response_data: dict, key: str, msg=''):
        result = (key in response_data)

        description = (
            'Response data from {url} must contain key "{key}".\n'
            'But it does not.\n'
            'Formatted response data:\n'
            '{formatted_data}'.format(
                url=r.url,
                formatted_data=json.dumps(response_data, indent="  "),
                key=key
            )
        )

        description = Assertions._add_msg(description, msg)

        assert result, description

    @staticmethod
    def assert_method_list_templates(r: requests.Response, templates: list, exact_match=False, code=200, msg=''):
        Assertions.assert_response_status_code(r=r, code=code, msg=msg)

        Assertions.assert_response_is_json(r=r, msg=msg)

        response_data = json.loads(r.text)

        print(response_data)

        result = ('templates' in response_data)

        description = (
            'Response data from {url} must contain key "templates".\n'
            'But it does not.\n'
            'Formatted response data:\n'
            '{formatted_data}'.format(
                url=r.url,
                formatted_data=json.dumps(response_data, indent="  ")
            )
        )

        description = Assertions._add_msg(description, msg)

        assert result, description

    @staticmethod
    def assert_method_delete_template(r: requests.Response, message='', code=200, msg=''):
        Assertions.assert_response_status_code(r=r, code=code, msg=msg)

        Assertions.assert_response_is_json(r=r, msg=msg)

        response_data = json.loads(r.text)

        Assertions.assert_response_data_has_key(r=r, response_data=response_data, key='message', msg=msg)

        result = (response_data['message'] == message)

        description = (
            'Response data from {url} must contain value "{message}" under key "message".\n'
            'But it does not.\n'
            'Formatted response data:\n'
            '{formatted_data}'.format(
                url=r.url,
                formatted_data=json.dumps(response_data, indent="  "),
                message=message
            )
        )

        description = Assertions._add_msg(description, msg)

        assert result, description

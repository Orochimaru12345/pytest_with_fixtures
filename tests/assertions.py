import json
import typing

import requests

APPLICATION_JSON = 'application/json'
rs = requests.Response


class Assertions(object):
    @staticmethod
    def _add_msg(description, msg):
        if msg != '':
            description = '\n' + msg + '.\n' + description
        return description

    @staticmethod
    def response_status_code(r: rs, code=200, msg=''):
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
    def response_is_json(r: rs, msg=''):
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
    def response_data_has_key(r: rs, response_data: dict, key: str, msg=''):
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
    def response_data_has_value(r: rs, response_data: dict, key: str, value: str, msg=''):
        Assertions.response_data_has_key(r=r, response_data=response_data, key=key, msg=msg)

        result = (response_data[key] == value)

        description = (
            'Response data from {url} must contain value "{value}" under key "message".\n'
            'But it does not.\n'
            'Formatted response data:\n'
            '{formatted_data}'.format(
                url=r.url,
                formatted_data=json.dumps(response_data, indent="  "),
                value=value
            )
        )

        description = Assertions._add_msg(description, msg)

        assert result, description

    @staticmethod
    def templates_list_response(r: rs, templates: list, exact_match=False, code=200, msg=''):
        Assertions.response_status_code(r=r, code=code, msg=msg)

        Assertions.response_is_json(r=r, msg=msg)

        response_data = json.loads(r.text)

        Assertions.response_data_has_key(r, response_data, 'templates', msg)

        # check required templates
        Assertions.value_type_is(r, response_data, 'templates', 'list')

        for t in templates:
            Assertions.value_in_collection(response_data['templates'], t, 'List of templates', msg=msg)

        if exact_match:
            for t in response_data['templates']:
                if t not in templates:
                    assert False, (
                        f'Unexpected template "{t}" found in list of templates\n'
                        f'List of templates:\n'
                        f'{json.dumps(response_data["templates"], indent="  ")}'
                    )

    @staticmethod
    def templates_delete_response(r: rs, message='', code=200, msg=''):
        Assertions.response_status_code(r=r, code=code, msg=msg)

        Assertions.response_is_json(r=r, msg=msg)

        response_data = json.loads(r.text)

        Assertions.response_data_has_key(r=r, response_data=response_data, key='message', msg=msg)

        Assertions.response_data_has_value(r=r, response_data=response_data, key='message', value=message, msg=msg)

    @staticmethod
    def templates_upload_response(r: rs, message='', code=201, msg=''):
        Assertions.response_status_code(r=r, code=code, msg=msg)

        Assertions.response_is_json(r=r, msg=msg)

        response_data = json.loads(r.text)

        Assertions.response_data_has_key(r=r, response_data=response_data, key='message', msg=msg)

        Assertions.response_data_has_value(r=r, response_data=response_data, key='message', value=message, msg=msg)

    @staticmethod
    def templates_install_response(r: rs, message='', code=200, msg=''):
        Assertions.response_status_code(r=r, code=code, msg=msg)

        Assertions.response_is_json(r=r, msg=msg)

        response_data = json.loads(r.text)

        Assertions.response_data_has_key(r=r, response_data=response_data, key='message', msg=msg)

        Assertions.response_data_has_value(r=r, response_data=response_data, key='message', value=message, msg=msg)

    @staticmethod
    def value_type_is(r: rs, response_data: dict, key: str, t='list', msg=''):
        result = (type(response_data[key]).__name__ == t)

        description = (
            f'In response data from {r.url} a value under key "{key}" must be of type "{t}".\n'
            f'But it is {type(response_data[key])}.\n'
            'Formatted response data:\n'
            f'{json.dumps(response_data, indent="  ")}'
        )

        description = Assertions._add_msg(description, msg)

        assert result, description

    @staticmethod
    def value_in_collection(coll: typing.Union[list, dict], value, coll_name, msg=''):
        result = (value in coll)
        description = (
            f'Collection "{coll_name}" does not have value {value}\n'
            f'Collection data:\n'
            f'{json.dumps(coll, indent="  ")}'
        )
        assert result, description

import pytest
import conftest

from assertions import Assertions as A

custom_ids = [
    'ok', 'simple_id', 's p a c e s', 'ID!', '№8', 'Ж-у-к', '@apt', '~', '`', "'", '"', '$',
    '%', '^', '&', '*', '(', ')', 'a-b.c@eee.com',
    '[', ']', '|', '{', '┳━┳ ノ( ゜-゜ノ)(╯°□°）╯︵ ┻━┻', 'MyNewTemplate', '-',
    'very_long_and_descriptive_template_name_for_the_case_when_long_name_is_the_only_option_01234567890'
]

invalid_ids = [  # special url characters
    '#hash', '/slash', '?question_mark', '#', '/', '?'
]

good_template_files = [
    'app_templates/template5.yaml',
    'app_templates/template1.yaml',
    'app_templates/template2.yaml',
    'app_templates/шаблон.yaml',
    'app_templates/e@mail.yaml',
    'app_templates/template6_no_optional_params.yaml',
    'app_templates/template8.yml',
]

invalid_templates_to_upload = [
    [
        'app_templates/template3_complete_mess.yaml',
        "Invalid template format\\!"
    ],
    [
        'app_templates/template4_missing_id.yaml',
        "No \"id\" field in {'label': 'Btn', 'link': 'https://www.example.org'}"
    ],
    [
        'app_templates/template7_missing_all.yaml',
        "No \"id\" field in {}"
    ],
    [
        'app_templates/no_yaml_for_you',
        "(Allowed file types are {('yml'|'yaml'), ('yml'|'yaml')})"  # regex
    ],
    [
        'app_templates/text.txt',
        "(Allowed file types are {('yml'|'yaml'), ('yml'|'yaml')})"  # regex
    ],
    [
        'app_templates/template9_missing_label_1.yaml',
        "Links without labels are not allowed. Error occurred in {'id': 100, 'link': 'https://www.example.org'}"
    ],
    [
        'app_templates/template9_missing_label_2.yaml',
        "ANY ERROR ABOUT MISSING LABEL"
    ],
]

invalid_templates_to_install = [
    [
        'app_templates/template3_complete_mess.yaml',
        "Invalid template format!"
    ],
    [
        'app_templates/template4_missing_id.yaml',
        "No \"id\" field in {'label': 'Btn', 'link': 'https://www.example.org'}"
    ],
    [
        'app_templates/template7_missing_all.yaml',
        "No \"id\" field in {}"
    ],
    [
        'app_templates/template9_missing_label_1.yaml',
        "Links without labels are not allowed. Error occurred in {'id': 100, 'link': 'https://www.example.org'}"
    ],
    [
        'app_templates/template9_missing_label_2.yaml',
        "ANY ERROR ABOUT MISSING LABEL"
    ],
]

template_files_to_delete = [
    'app_templates/delete/delete1.yaml'
]


@pytest.mark.ignores_app_state
class TestApp(object):
    # noinspection PyMethodMayBeStatic
    def _verify_tmpl_id_in_list(self, app: conftest.App, tmpl_id: str):
        r = app.list_templates()
        A.templates_list_response(
            r, [tmpl_id], msg='List of templates must have id of our new template'
        )

    # noinspection PyMethodMayBeStatic
    def _tmpl_id_from_file_name(self, tmpl_file: str):
        # drop path
        name = (tmpl_file.split('/')[-1])
        # drop extension
        name = ''.join(name.split('.')[0:-1])
        # drop special characters
        name = name.replace('@', '')
        print('NAME NAME NAME' + name)
        return name

    # upload
    @pytest.mark.parametrize('tmpl_file', good_template_files)
    def test_upload_templates(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_file
    ):
        tmpl_id = self._tmpl_id_from_file_name(tmpl_file)

        # upload
        r = app.upload_template(tmpl_file)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id}',
            msg='Upload a template with default tmpl_id'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id)

    @pytest.mark.parametrize('tmpl_id', custom_ids)
    def test_upload_templates_by_different_custom_ids(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_id
    ):
        # upload
        r = app.upload_template('app_templates/template1.yaml', tmpl_id)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id.lower()}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id}".'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id.lower())

    @pytest.mark.parametrize(['tmpl_file', 'err_msg'], invalid_templates_to_upload)
    def test_upload_invalid_templates(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_file, err_msg
    ):
        r = app.upload_template(tmpl_file)
        A.templates_upload_response(
            r,
            err_msg,
            code=400,
            msg='We should not be able to upload wrong templates',
            regex=True
        )

    @pytest.mark.parametrize('tmpl_id', invalid_ids)
    def test_upload_templates_by_invalid_ids(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_id
    ):
        tmpl_file = 'app_templates/template1.yaml'
        r = app.upload_template(tmpl_file, tmpl_id)
        A.templates_upload_response(
            r,
            'ANY_ERROR_ABOUT_BAD_ID',
            msg=(
                f'In our API we should not be able to use dangerous ids.\n'
                f'They can backfire later when we put them into URLs in such way: /templates/{tmpl_id}/install'
            )
        )

    # install
    @pytest.mark.parametrize('tmpl_file', good_template_files)
    def test_install_templates(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_file
    ):
        tmpl_id = self._tmpl_id_from_file_name(tmpl_file)

        # upload
        r = app.upload_template(tmpl_file)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id}".'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id)
        # install
        r = app.install_template(tmpl_id)
        A.templates_install_response(
            r,
            f'Template with tmpl_id={tmpl_id} successfully installed!',
            msg='We should be able to install a template by default tmpl_id'
        )

    @pytest.mark.parametrize('tmpl_id', custom_ids)
    def test_install_templates_by_different_custom_ids(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_id
    ):
        # upload
        r = app.upload_template('app_templates/template1.yaml', tmpl_id=tmpl_id)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id.lower()}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id}".'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id.lower())
        # install
        r = app.install_template(tmpl_id.lower())
        A.templates_install_response(
            r,
            f'Template with tmpl_id={tmpl_id.lower()} successfully installed!',
            msg=f'We should be able to install a template by id {tmpl_id}'
        )

    @pytest.mark.parametrize(['tmpl_file', 'err_msg'], invalid_templates_to_install)
    def test_install_invalid_templates(
            self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_file, err_msg
    ):
        tmpl_id = self._tmpl_id_from_file_name(tmpl_file)

        # upload
        r = app.upload_template(tmpl_file)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id}',
            msg='Upload invalid template to install it afterwards'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id)

        # install
        r = app.install_template(tmpl_id)
        A.templates_install_response(
            r=r,
            code=400,
            msg='We should not be able to install an invalid template.',
            message=err_msg
        )

    def test_install_unknown_template(self, app: conftest.App, docker_container: conftest.DockerContainer):
        tmpl_id = 'install_unknown_template'

        r = app.install_template(tmpl_id)

        A.templates_install_response(
            r,
            message=f'No template with tmpl_id={tmpl_id} found!',
            code=404,
            msg='App must return an error if you try install a template which is not exists'
        )

    # delete
    @pytest.mark.parametrize('tmpl_file', template_files_to_delete)
    def test_delete_templates(self, app: conftest.App, docker_container: conftest.DockerContainer, tmpl_file):
        tmpl_id = self._tmpl_id_from_file_name(tmpl_file)

        # upload
        r = app.upload_template(tmpl_file)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id}".'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id)
        # install
        r = app.delete_template(tmpl_id)
        A.templates_delete_response(
            r,
            f'Template with tmpl_id={tmpl_id} successfully deleted!',
            msg='We should be able to delete a template by default tmpl_id'
        )

    @pytest.mark.parametrize('tmpl_id', custom_ids)
    def test_delete_templates_by_different_custom_ids(self, app: conftest.App,
                                                      docker_container: conftest.DockerContainer, tmpl_id):
        # upload
        r = app.upload_template('app_templates/delete/delete2.yaml', tmpl_id=tmpl_id)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id.lower()}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id}".'
        )
        # verify
        self._verify_tmpl_id_in_list(app, tmpl_id.lower())
        # install
        r = app.delete_template(tmpl_id.lower())
        A.templates_delete_response(
            r,
            f'Template with tmpl_id={tmpl_id.lower()} successfully deleted!',
            msg=f'We should be able to install a template by id {tmpl_id}'
        )

    def test_delete_unknown_template(self, app: conftest.App, docker_container: conftest.DockerContainer):
        tmpl_id = 'delete_unknown_template'

        r = app.delete_template(tmpl_id)
        A.templates_delete_response(
            r,
            message=f'No template with tmpl_id={tmpl_id} found!',
            code=404,
            msg='App must return an error if you try delete a template which is not exists'
        )

    # list
    def test_list_of_templates(self, app: conftest.App, docker_container: conftest.DockerContainer):
        # upload
        tmpl_id_1 = 'template_for_list_1'
        r = app.upload_template('app_templates/list/template_for_list_1.yaml')
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id_1}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id_1}".'
        )
        tmpl_id_2 = 'template-for-list-2'
        r = app.upload_template('app_templates/list/template_for_list_2.yml', tmpl_id_2)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id_2}',
            msg=f'Upload a simple template with tmpl_id = "{tmpl_id_2}".'
        )
        # list
        r = app.list_templates()
        A.templates_list_response(
            r,
            [tmpl_id_1, tmpl_id_2],
            msg='Both our templates must be visible in the templates list'
        )

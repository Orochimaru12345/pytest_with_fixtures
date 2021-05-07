import pytest
import conftest

from assertions import Assertions as A


@pytest.mark.requires_fresh_app
class TestFreshAppGetTemplates(object):
    def test_get_templates(self, app: conftest.App, docker_container: conftest.DockerContainer):
        r = app.list_templates()
        A.templates_list_response(
            r=r,
            templates=[],
            exact_match=True,
            msg=(
                'When app is just started'
                ' and does not have any templates'
                ' it must return empty JSON list [] with key "templates"'
            )
        )


@pytest.mark.requires_fresh_app
class TestFreshAppDeleteTemplate(object):
    def test_delete_template(self, app: conftest.App, docker_container: conftest.DockerContainer):
        tmpl_id = 'd_tmpl'
        r = app.delete_template(tmpl_id)
        A.templates_delete_response(
            r=r,
            code=404,
            message=f'No template with tmpl_id={tmpl_id} found!',
            msg=(
                'When app is just started'
                ' and does not have any templates'
                ' it must not fall on attempt to delete a template\n'
                'It must return a message which looks like "No template with tmpl_id=<tmpl_id> found!"'
            )
        )


@pytest.mark.requires_fresh_app
class TestFreshAppUploadTemplate(object):
    def test_upload_template(self, app: conftest.App, docker_container: conftest.DockerContainer):
        tmpl_id = "u_template"
        r = app.upload_template('app_templates/template1.yaml', tmpl_id)
        A.templates_upload_response(
            r,
            f'Template successfully uploaded. tmpl_id={tmpl_id}',
            msg='Upload a template'
        )

        r = app.list_templates()
        A.templates_list_response(
            r, [tmpl_id], exact_match=True, msg='List of templates must have one item which is id of our new template'
        )


@pytest.mark.requires_fresh_app
class TestFreshAppInstallTemplate(object):
    def test_delete_template(self, app: conftest.App, docker_container: conftest.DockerContainer):
        tmpl_id = 'd_tmpl'
        r = app.install_template(tmpl_id)
        A.templates_delete_response(
            r=r,
            code=404,
            message=f'No template with tmpl_id={tmpl_id} found!',
            msg=(
                'When app is just started'
                ' and does not have any templates'
                ' it must not fall on attempt to install a template\n'
                'It must return a message which looks like "No template with tmpl_id=<tmpl_id> found!"'
            )
        )

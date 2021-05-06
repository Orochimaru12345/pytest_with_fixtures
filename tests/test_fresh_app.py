import pytest
import conftest

from assertions import Assertions as A


@pytest.mark.requires_fresh_app
class TestFreshAppGetTemplates(object):
    def test_get_templates(self, app: conftest.App):
        r = app.list_templates()
        A.assert_method_list_templates(
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
    def test_delete_template(self, app: conftest.App):
        tmpl_id = '1'
        r = app.delete_template(tmpl_id)
        A.assert_method_delete_template(
            r=r,
            code=404,
            message="No template with tmpl_id=1 found!",
            msg=(
                'When app is just started'
                ' and does not have any templates'
                ' it must not fall on attempt to delete a template\n'
                'It must return a message which looks like "No template with tmpl_id=<tmpl_id> found!"'
            )
        )


@pytest.mark.requires_fresh_app
class TestFreshAppUploadTemplate(object):
    pass


@pytest.mark.requires_fresh_app
class TestFreshAppInstallTemplate(object):
    pass

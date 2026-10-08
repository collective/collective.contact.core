from plone import api


def v21(context):
    setup = api.portal.get_tool("portal_setup")
    setup.runAllImportStepsFromProfile("profile-imio.fpaudit:default")
    setup.runImportStepFromProfile("profile-collective.contact.core:default", "plone.app.registry")

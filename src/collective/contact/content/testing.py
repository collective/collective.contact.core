from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.contact.content


COLLECTIVE_CONTACT_CONTENT = PloneWithPackageLayer(
    zcml_package=collective.contact.content,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.contact.content:testing',
    name="COLLECTIVE_CONTACT_CONTENT")

COLLECTIVE_CONTACT_CONTENT_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_CONTACT_CONTENT, ),
    name="COLLECTIVE_CONTACT_CONTENT_INTEGRATION")

COLLECTIVE_CONTACT_CONTENT_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CONTENT, ),
    name="COLLECTIVE_CONTACT_CONTENT_FUNCTIONAL")

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from ecreall.helpers.testing import member as memberhelpers

import collective.contact.content


USERDEFS = [
        {'user': 'manager', 'roles': ('Manager', 'Member'), 'groups': ()},
        {'user': 'member', 'roles': ('Member', ), 'groups': ()},
        ]


class ContactContentLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.contact.content:testing')
        memberhelpers.createMembers(portal, USERDEFS)


COLLECTIVE_CONTACT_CONTENT = ContactContentLayer(
    zcml_package=collective.contact.content,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.contact.content:testing',
    name="COLLECTIVE_CONTACT_CONTENT")

INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_CONTACT_CONTENT, ),
    name="INTEGRATION")

FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CONTENT, ),
    name="FUNCTIONAL")

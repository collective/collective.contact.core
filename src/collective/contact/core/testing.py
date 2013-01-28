# -*- coding: utf8 -*-

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.contact.core


class ContactContentLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.contact.core:testing')
        # insert some test data
        self.applyProfile(portal, 'collective.contact.core:test_data')


COLLECTIVE_CONTACT_CORE = ContactContentLayer(
    zcml_package=collective.contact.core,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.contact.core:testing',
    name="COLLECTIVE_CONTACT_CORE")

INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_CONTACT_CORE, ),
    name="INTEGRATION")

FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CORE, ),
    name="FUNCTIONAL")

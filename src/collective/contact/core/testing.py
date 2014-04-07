# -*- coding: utf8 -*-

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from plone.testing import z2

import collective.contact.core


class ContactContentLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.contact.core:testing')
        # insert some test data
        self.applyProfile(portal, 'collective.contact.core:test_data')
        setRoles(portal, TEST_USER_ID, ['Manager'])


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

ACCEPTANCE = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CORE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ACCEPTANCE")

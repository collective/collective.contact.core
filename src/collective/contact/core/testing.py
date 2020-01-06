# -*- coding: utf8 -*-

from collective.contact.core.setuphandlers import create_test_contact_data
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2

import collective.contact.core
import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PA_CONTENTTYPES = False
else:
    HAS_PA_CONTENTTYPES = True


class ContactContentLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        super(ContactContentLayer, self).setUpPloneSite(portal)
        assert portal.portal_quickinstaller.isProductInstalled('collective.contact.core')

        # Plone 5 support
        if HAS_PA_CONTENTTYPES:
            self.applyProfile(portal, 'plone.app.contenttypes:default')

        self.applyProfile(portal, 'collective.contact.core:testing')
        # # insert some test data
        # self.applyProfile(portal, 'collective.contact.core:test_data')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        create_test_contact_data(portal)
        # transaction.commit()
        assert portal.portal_quickinstaller.isProductInstalled('collective.contact.core')


FIXTURE = ContactContentLayer(
    zcml_package=collective.contact.core,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.contact.core:testing',
    name="FIXTURE")

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="INTEGRATION")

ACCEPTANCE = FunctionalTesting(
    bases=(FIXTURE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ACCEPTANCE")

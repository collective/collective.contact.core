# -*- coding: utf8 -*-

from collective.contact.core.setuphandlers import create_test_contact_data
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2

import collective.contact.core
import pkg_resources


class CollectiveContactCoreLayer(PloneSandboxLayer):

    defaultBases = (
        PLONE_APP_CONTENTTYPES_FIXTURE,
    )

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.contact.widget)
        self.loadZCML(package=collective.contact.core)
        self.loadZCML(name='testing.zcml', package=collective.contact.core)

    def setUpPloneSite(self, portal):

        self.applyProfile(portal, 'collective.contact.core:testing')
        # # insert some test data
        setRoles(portal, TEST_USER_ID, ['Manager'])
        create_test_contact_data(portal)


COLLECTIVE_CONTACT_CORE_FIXTURE = CollectiveContactCoreLayer()


COLLECTIVE_CONTACT_CORE_ACCEPTANCE_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTACT_CORE_FIXTURE,),
    name='CollectiveContactCoreLayer:IntegrationTesting',
)


COLLECTIVE_CONTACT_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CORE_FIXTURE,),
    name='CollectiveContactCoreLayer:FunctionalTesting',
)


COLLECTIVE_CONTACT_CORE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_CONTACT_CORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveContactCoreLayer:AcceptanceTesting',
)

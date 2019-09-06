# -*- coding: utf8 -*-

from collective.contact.core.testing import INTEGRATION
from ecreall.helpers.testing.search import BaseSearchTest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME

import unittest


class TestUtils(unittest.TestCase, BaseSearchTest):

    layer = INTEGRATION

    def setUp(self):
        super(TestUtils, self).setUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        mydirectory = self.portal['mydirectory']
        self.degaulle = mydirectory['degaulle']

    def test_recordModified(self):
        """ """
        self.login(TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        dguid = self.degaulle.UID()
        record_name = 'collective.contact.core.interfaces.IContactCoreParameters.contact_source_metadata_content'
        self.assertEqual(api.portal.get_registry_record(record_name), u'{gft}')
        self.assertEqual(self.getBrain(dguid).contact_source, self.degaulle.get_full_title())
        # we change registry
        api.portal.set_registry_record(record_name, u'{gft} from {city} on {email}')
        # metadata has been updated
        self.assertEqual(self.getBrain(dguid).contact_source,
                         u'Général Charles De Gaulle from Colombey les deux églises on charles.de.gaulle@private.com')

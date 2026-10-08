# -*- coding: utf8 -*-

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.tests.base import BaseTest
from plone import api
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class TestUtils(unittest.TestCase, BaseTest):

    layer = INTEGRATION

    def setUp(self):
        super(TestUtils, self).setUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        mydirectory = self.portal['mydirectory']
        self.degaulle = mydirectory['degaulle']
        self.rambo = mydirectory['rambo']
        self.brigadelh = mydirectory['armeedeterre']['corpsa']['divisionalpha']['regimenth']['brigadelh']

    def test_relation_unindex(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        held_brigadelh = self.rambo["brigadelh"]
        int_id = intids.getId(held_brigadelh)
        rels = catalog.findRelations({"from_id": int_id})
        self.assertEqual(len([i for i in rels]), 1)
        brigadelh_id = intids.getId(self.brigadelh)
        self.assertTrue(list(catalog.findRelations({"to_id": brigadelh_id})))
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(self.brigadelh)
        api.content.delete(self.brigadelh, check_linkintegrity=False)
        rels = catalog.findRelations({"from_id": int_id})
        self.assertEqual(len([i for i in rels]), 0)
        # no broken relation is left pointing to the deleted organization
        self.assertEqual(list(catalog.findRelations({"to_id": brigadelh_id})), [])

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

    def test_linkintegrity_breach_on_referenced_contact(self):
        """Plone linkintegrity reports contact relations as breaches."""
        mydirectory = self.portal['mydirectory']
        sergent_lh = mydirectory.unrestrictedTraverse('armeedeterre/corpsa/divisionalpha/regimenth/brigadelh/sergent_lh')
        view = self.portal.restrictedTraverse('@@delete_confirmation_info')
        sources = [s['uid'] for b in view.get_breaches([sergent_lh]) for s in b['sources']]
        self.assertEqual(sources, [mydirectory['pepper']['sergent_pepper'].UID()])

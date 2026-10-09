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
from zope.lifecycleevent import modified

import unittest


class TestUtils(unittest.TestCase, BaseTest):

    layer = INTEGRATION

    def setUp(self):
        super(TestUtils, self).setUp()
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        mydirectory = self.portal["mydirectory"]
        self.degaulle = mydirectory["degaulle"]
        self.rambo = mydirectory["rambo"]
        self.brigadelh = mydirectory["armeedeterre"]["corpsa"]["divisionalpha"]["regimenth"]["brigadelh"]
        self.armeedeterre = mydirectory["armeedeterre"]
        self.login(TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def search(self, text, portal_type):
        return sorted([brain.getPath() for brain in api.content.find(SearchableText=text, portal_type=portal_type)])

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
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        dguid = self.degaulle.UID()
        record_name = "collective.contact.core.interfaces.IContactCoreParameters.contact_source_metadata_content"
        self.assertEqual(api.portal.get_registry_record(record_name), "{gft}")
        self.assertEqual(self.getBrain(dguid).contact_source, self.degaulle.get_full_title())
        # we change registry
        api.portal.set_registry_record(record_name, "{gft} from {city} on {email}")
        # metadata has been updated
        self.assertEqual(
            self.getBrain(dguid).contact_source,
            "Général Charles De Gaulle from Colombey les deux églises on charles.de.gaulle@private.com",
        )

    def test_linkintegrity_breach_on_referenced_contact(self):
        """Plone linkintegrity reports contact relations as breaches."""
        mydirectory = self.portal["mydirectory"]
        sergent_lh = mydirectory.unrestrictedTraverse(
            "armeedeterre/corpsa/divisionalpha/regimenth/brigadelh/sergent_lh"
        )
        view = self.portal.restrictedTraverse("@@delete_confirmation_info")
        sources = [s["uid"] for b in view.get_breaches([sergent_lh]) for s in b["sources"]]
        self.assertEqual(sources, [mydirectory["pepper"]["sergent_pepper"].UID()])

    def test_update_related_with_person(self):
        self.assertEqual(self.search("Charlie", "held_position"), [])
        self.degaulle.firstname = "Charlie"
        modified(self.degaulle)
        # held positions are found with the new person name
        self.assertEqual(
            self.search("Charlie", "held_position"),
            ["/plone/mydirectory/degaulle/adt", "/plone/mydirectory/degaulle/gadt"],
        )

    def test_update_related_with_position(self):
        general_adt = self.armeedeterre["general_adt"]
        self.assertEqual(self.search("Marshal", "held_position"), [])
        general_adt.title = "Marshal"
        modified(general_adt)
        # the held position and its person are found with the new position title
        self.assertEqual(self.search("Marshal", "held_position"), ["/plone/mydirectory/degaulle/gadt"])
        self.assertEqual(self.search("Marshal", "person"), ["/plone/mydirectory/degaulle"])

    def test_update_related_with_held_position(self):
        gadt = self.degaulle["gadt"]
        self.assertEqual(self.search("Ambassador", "person"), [])
        gadt.label = "Ambassador"
        modified(gadt)
        # the person is found with the new held position label
        self.assertEqual(self.search("Ambassador", "person"), ["/plone/mydirectory/degaulle"])

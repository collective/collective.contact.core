# -*- coding: utf8 -*-
from collective.contact.core.testing import INTEGRATION
from collective.contact.core.vocabularies import get_directory
from collective.contact.core.vocabularies import get_vocabulary
from collective.contact.core.vocabularies import NoDirectoryFound
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest
from zope.schema.interfaces import IVocabularyFactory

import unittest


def terms(vocabulary):
    return [(term.value, term.token, term.title) for term in vocabulary]


class TestVocabularies(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.mydirectory = self.portal["mydirectory"]
        self.armeedeterre = self.mydirectory["armeedeterre"]
        self.corpsa = self.armeedeterre["corpsa"]

    def test_get_directory(self):
        self.assertEqual(get_directory(self.mydirectory), self.mydirectory)
        self.assertEqual(get_directory(self.mydirectory["degaulle"]["gadt"]), self.mydirectory)
        self.assertEqual(get_directory(self.corpsa), self.mydirectory)
        with self.assertRaises(NoDirectoryFound):
            get_directory(None)
        with self.assertRaises(NoDirectoryFound):
            get_directory(self.portal)

    def test_get_vocabulary(self):
        vocabulary = get_vocabulary(
            [{"name": "Général", "token": "general"}, {"name": "Sergeant", "token": "sergeant"}]
        )
        self.assertEqual(terms(vocabulary), [("general", "general", "Général"), ("sergeant", "sergeant", "Sergeant")])
        self.assertEqual(terms(get_vocabulary([])), [])

    def test_PositionTypes(self):
        factory = getUtility(IVocabularyFactory, "PositionTypes")
        expected = ["general", "sergeant", "colonel", "lieutenant", "captain", "admiral"]
        self.assertEqual([term.value for term in factory(self.armeedeterre["general_adt"])], expected)
        self.assertEqual(factory(self.mydirectory).getTerm("captain").title, "Captain")
        # outside a directory
        self.assertEqual(terms(factory(self.portal)), [])

    def test_OrganizationTypesOrLevels(self):
        factory = getUtility(IVocabularyFactory, "OrganizationTypesOrLevels")
        organization_types = ["navy", "army", "air_force"]
        organization_levels = ["corps", "division", "regiment", "squad"]
        self.addCleanup(setRequest, getRequest())
        setRequest(self.request)
        # edit or view: depends on the organization container
        self.request["URL"] = self.armeedeterre.absolute_url() + "/edit"
        self.assertEqual([term.value for term in factory(self.armeedeterre)], organization_types)
        self.request["URL"] = self.corpsa.absolute_url() + "/edit"
        self.assertEqual([term.value for term in factory(self.corpsa)], organization_levels)
        # add: depends on the context, the future container
        self.request["URL"] = self.mydirectory.absolute_url() + "/++add++organization"
        self.assertEqual([term.value for term in factory(self.mydirectory)], organization_types)
        self.request["URL"] = self.corpsa.absolute_url() + "/++add++organization"
        self.assertEqual([term.value for term in factory(self.corpsa)], organization_levels)
        # outside a directory
        self.assertEqual(terms(factory(self.portal)), [])

    def test_Genders(self):
        factory = getUtility(IVocabularyFactory, "Genders")
        vocabulary = factory(self.portal)
        self.assertEqual(sorted([term.value for term in vocabulary]), ["F", "M"])
        self.assertEqual(vocabulary.getTerm("F").title, "Female")
        self.assertEqual(vocabulary.getTerm("M").title, "Male")

    def test_AuditTypes(self):
        factory = getUtility(IVocabularyFactory, "collective.contact.core.audit_types")
        values = [term.value for term in factory(self.portal)]
        # types having the contact details behavior
        for portal_type in ("organization", "person", "position", "held_position", "testtype"):
            self.assertIn(portal_type, values)
        self.assertNotIn("directory", values)
        self.assertEqual(factory(self.portal).getTerm("held_position").title, "Held position")

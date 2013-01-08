# -*- coding: utf8 -*-

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from ecreall.helpers.testing.base import BaseTest

from collective.contact.content.testing import INTEGRATION
from collective.contact.content.indexers import held_position_searchable_text


class TestSearch(unittest.TestCase, BaseTest):
    """Tests search"""

    layer = INTEGRATION

    def setUp(self):
        super(TestSearch, self).setUp()
        self.portal = self.layer['portal']
        self.mydirectory = self.portal['mydirectory']
        self.degaulle = self.mydirectory['degaulle']
        self.pepper = self.mydirectory['pepper']
        self.armeedeterre = self.mydirectory['armeedeterre']
        self.general_adt = self.armeedeterre['general_adt']
        self.corpsa = self.armeedeterre['corpsa']
        self.corpsb = self.armeedeterre['corpsb']
        self.gadt = self.degaulle['gadt']
        self.sergent_pepper = self.pepper['sergent_pepper']

    def test_indexers(self):
        gadt = self.gadt
        self.assertEqual(held_position_searchable_text(gadt)(),\
                         "Général de l'armée de terre Armée de terre")
        sergent_pepper = self.sergent_pepper
        self.assertEqual(held_position_searchable_text(sergent_pepper)(),\
                         "Sergent de la brigade LH Brigade LH Régiment H Division Alpha Corps A Armée de terre")

    def test_searchable_fields(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        results = catalog.searchResults(SearchableText='Gaulle')
        self.assertEqual(len(results), 1)
        results = catalog.searchResults(SearchableText='Général')
        self.assertEqual(len(results), 2)
        results = catalog.searchResults(SearchableText='Corps')
        self.assertEqual(len(results), 3)
        results_objects = [res.getObject() for res in results]
        self.assertIn(self.corpsa, results_objects)
        self.assertIn(self.corpsb, results_objects)
        self.assertIn(self.sergent_pepper, results_objects)
        results = catalog.searchResults(SearchableText='armée')
        self.assertEqual(len(results), 5)
        results = catalog.searchResults(SearchableText='beta')
        self.assertEqual(len(results), 1)
        results = catalog.searchResults(SearchableText='régiment')
        self.assertEqual(len(results), 2)
        results = catalog.searchResults(SearchableText='brigade')
        self.assertEqual(len(results), 3)

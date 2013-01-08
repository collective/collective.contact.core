# -*- coding: utf8 -*-

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from ecreall.helpers.testing.base import BaseTest

from collective.contact.content.testing import INTEGRATION
from collective.contact.content.indexers import held_position_searchable_text,\
    organization_searchable_text


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
        self.divisionalpha = self.corpsa['divisionalpha']
        self.divisionbeta = self.corpsa['divisionbeta']
        self.regimenth = self.divisionalpha['regimenth']
        self.brigadelh = self.regimenth['brigadelh']
        self.gadt = self.degaulle['gadt']
        self.sergent_pepper = self.pepper['sergent_pepper']

    def test_indexers(self):
        divisionalpha = self.divisionalpha
        self.assertEqual(organization_searchable_text(divisionalpha)(),\
                         "Armée de terre Corps A Division Alpha")
        gadt = self.gadt
        self.assertEqual(held_position_searchable_text(gadt)(),\
                         "Général de l'armée de terre Armée de terre")
        sergent_pepper = self.sergent_pepper
        self.assertEqual(held_position_searchable_text(sergent_pepper)(),\
                         "Sergent de la brigade LH Armée de terre Corps A Division Alpha Régiment H Brigade LH")

    def test_searchable_fields(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        results = catalog.searchResults(SearchableText='Gaulle')
        self.assertEqual(len(results), 1)
        results = catalog.searchResults(SearchableText='Général')
        self.assertEqual(len(results), 2)
        results = catalog.searchResults(SearchableText='Corps')
        self.assertEqual(len(results), 7)
        results_objects = [res.getObject() for res in results]
        self.assertIn(self.corpsa, results_objects)
        self.assertIn(self.corpsb, results_objects)
        self.assertIn(self.divisionalpha, results_objects)
        self.assertIn(self.divisionbeta, results_objects)
        self.assertIn(self.regimenth, results_objects)
        self.assertIn(self.brigadelh, results_objects)
        self.assertIn(self.sergent_pepper, results_objects)
        results = catalog.searchResults(SearchableText='armée')
        self.assertEqual(len(results), 11)
        results = catalog.searchResults(SearchableText='beta')
        self.assertEqual(len(results), 1)
        results = catalog.searchResults(SearchableText='régiment')
        self.assertEqual(len(results), 3)
        results = catalog.searchResults(SearchableText='brigade')
        self.assertEqual(len(results), 3)

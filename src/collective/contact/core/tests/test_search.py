# -*- coding: utf8 -*-

from collective.contact.core.indexers import end_date
from collective.contact.core.indexers import held_position_sortable_title
from collective.contact.core.indexers import person_sortable_title
from collective.contact.core.indexers import start_date
from collective.contact.core.testing import INTEGRATION
from ecreall.helpers.testing.base import BaseTest
from plone import api

import datetime
import unittest


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
        pc = self.portal.portal_catalog
        index = pc._catalog.getIndex("SearchableText")
        # check organization searchable text
        rid = pc(UID=self.divisionalpha.UID())[0].getRID()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['armee', 'de', 'terre', 'corps', 'a', 'division', 'alpha'])
        # check position searchable text
        rid = pc(UID=self.general_adt.UID())[0].getRID()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['general', 'de', 'l', 'armee', 'de', 'terre', 'armee', 'de', 'terre',
                                       'general', 'armees', 'fr'])
        # check held position searchable text
        rid = pc(UID=self.gadt.UID())[0].getRID()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['general', 'charles', 'de', 'gaulle', 'general', 'de', 'l', 'armee', 'de',
                                       'terre', 'armee', 'de', 'terre', 'emissaire', 'otan'])
        rid = pc(UID=self.sergent_pepper.UID())[0].getRID()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['mister', 'pepper', 'sergent', 'de', 'la', 'brigade', 'lh', 'armee', 'de',
                                       'terre', 'corps', 'a', 'division', 'alpha', 'regiment', 'h', 'brigade', 'lh',
                                       'sgt', 'pepper', 'armees', 'fr'])
        # check person searchable text
        rid = pc(UID=self.degaulle.UID())[0].getRID()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['general', 'charles', 'de', 'gaulle', 'charles', 'de', 'gaulle', 'private',
                                       'com', 'general', 'charles', 'de', 'gaulle', 'armee', 'de', 'terre', 'general',
                                       'charles', 'de', 'gaulle', 'general', 'de', 'l', 'armee', 'de', 'terre',
                                       'armee', 'de', 'terre', 'emissaire', 'otan'])

        # check others
        pepper = self.pepper
        self.assertEqual(person_sortable_title(pepper)(),
                         "pepper")
        idxr = held_position_sortable_title(self.sergent_pepper)
        self.assertEqual(idxr(),
                         u'pepper-sergent-de-la-brigade-lh-armee-de-terre-corps-a')
        degaulle = self.degaulle
        self.assertEqual(person_sortable_title(degaulle)(),
                         'de-gaulle-charles')
        self.assertEqual(start_date(self.sergent_pepper)(), datetime.date(1980, 6, 5))
        self.assertEqual(end_date(self.sergent_pepper)(), datetime.date(2100, 1, 1))
        self.assertEqual(end_date(self.gadt)(), datetime.date(1970, 11, 9))
        self.assertEqual(start_date(self.mydirectory['draper']['captain_crunch'])(),
                         self.mydirectory['draper']['captain_crunch'].created())

    def test_searchable_fields(self):
        catalog = api.portal.get_tool('portal_catalog')
        results = catalog.searchResults(SearchableText='Gaulle')
        self.assertEqual(len(results), 3)
        results = catalog.searchResults(SearchableText='Général')
        self.assertEqual(len(results), 4)
        results = catalog.searchResults(SearchableText='Corps')
        self.assertEqual(len(results), 13)
        results_objects = [res.getObject() for res in results]
        self.assertIn(self.corpsa, results_objects)
        self.assertIn(self.corpsb, results_objects)
        self.assertIn(self.divisionalpha, results_objects)
        self.assertIn(self.divisionbeta, results_objects)
        self.assertIn(self.regimenth, results_objects)
        self.assertIn(self.brigadelh, results_objects)
        self.assertIn(self.sergent_pepper, results_objects)
        results = catalog.searchResults(SearchableText='armée')
        self.assertEqual(len(results), 18)
        results = catalog.searchResults(SearchableText='beta')
        self.assertEqual(len(results), 3)
        results = catalog.searchResults(SearchableText='régiment')
        self.assertEqual(len(results), 6)
        results = catalog.searchResults(SearchableText='brigade')
        self.assertEqual(len(results), 6)
        results = catalog.searchResults(SearchableText='Émissaire')
        self.assertEqual(len(results), 2)
        results = catalog.searchResults(portal_type='held_position')
        self.assertEqual(len(results), 6)
        results = catalog.searchResults(portal_type='held_position',
                                        start={'query': datetime.date(1981, 1, 1), 'range': 'min'})
        self.assertEqual(len(results), 3)
        results = catalog.searchResults(portal_type='held_position',
                                        end={'query': datetime.date(1971, 1, 1), 'range': 'max'})
        self.assertEqual(len(results), 2)
        restults = catalog.searchResults(
            SearchableText='charles.de.gaulle@private.com')
        self.assertEqual(len(restults), 1)
        self.assertEqual(restults[0].getPath(), '/plone/mydirectory/degaulle')
        results = catalog.searchResults(SearchableText='BE123456789')
        self.assertEqual(len(results), 1)

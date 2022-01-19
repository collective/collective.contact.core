# -*- coding: utf8 -*-

from collective.contact.core.behaviors import IRelatedOrganizations
from collective.contact.core.testing import INTEGRATION
from ecreall.helpers.testing.base import BaseTest
from z3c.relationfield.relation import RelationValue
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds

import unittest


class TestSearch(unittest.TestCase, BaseTest):
    """Tests realted organizations"""

    layer = INTEGRATION

    def setUp(self):
        super(TestSearch, self).setUp()
        self.portal = self.layer['portal']
        self.mydirectory = self.portal['mydirectory']
        self.armeedeterre = self.mydirectory['armeedeterre']
        self.corpsa = self.armeedeterre['corpsa']
        self.divisionalpha = self.corpsa['divisionalpha']
        self.divisionbeta = self.corpsa['divisionbeta']

    def test_related_searchable_text(self):
        pc = self.portal.portal_catalog
        index = pc._catalog.getIndex("SearchableText")
        rid = pc(UID=self.divisionalpha.UID())[0].getRID()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['armee', 'de', 'terre', 'corps', 'a', 'division', 'alpha'])

        intids = getUtility(IIntIds)
        alsoProvides(self.divisionalpha, IRelatedOrganizations)
        self.divisionalpha.related_organizations = [
            RelationValue(intids.getId(self.divisionbeta)),
        ]
        self.divisionalpha.reindexObject()
        indexed = index.getEntryForObject(rid, default=[])
        self.assertListEqual(indexed, ['armee', 'de', 'terre', 'corps', 'a', 'division', 'beta', 'armee', 'de',
                                       'terre', 'corps', 'a', 'division', 'alpha'])

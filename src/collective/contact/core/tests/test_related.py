# -*- coding: utf8 -*-

from ecreall.helpers.testing.base import BaseTest
from plone import api
import unittest2 as unittest
from z3c.relationfield.relation import RelationValue
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.interface import alsoProvides

from collective.contact.core.behaviors import IRelatedOrganizations
from collective.contact.core.testing import INTEGRATION
from collective.contact.core.indexers import organization_searchable_text


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
        self.assertEqual(organization_searchable_text(self.divisionalpha)(),
            u"Armée de terre Corps A Division Alpha")

        intids = getUtility(IIntIds)
        alsoProvides(self.divisionalpha, IRelatedOrganizations)
        self.divisionalpha.related_organizations = [
            RelationValue(intids.getId(self.divisionbeta)),
        ]
        self.assertEqual(organization_searchable_text(self.divisionalpha)(),
            u'Armée de terre Corps A Division Beta Armée de terre Corps A Division Alpha')

# -*- coding: utf8 -*-

import unittest2 as unittest

import datetime

from ecreall.helpers.testing.base import BaseTest

from collective.contact.content.testing import INTEGRATION


class TestContentTypes(unittest.TestCase, BaseTest):
    """Tests new content types"""

    layer = INTEGRATION

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.portal = self.layer['portal']
        self.mydirectory = self.portal['mydirectory']
        self.degaulle = self.mydirectory['degaulle']
        self.armeedeterre = self.mydirectory['armeedeterre']
        self.general_adt = self.armeedeterre['general_adt']

    def test_directory(self):
        self.assertIn('mydirectory', self.portal)
        mydirectory = self.portal['mydirectory']
        self.assertEqual('Military directory', mydirectory.Title())
        self.assertIn({'name': 'Colonel', 'token': 'colonel'},
                      mydirectory.position_types)
        self.assertIn({'name': 'Air force', 'token': 'air_force'},
                      mydirectory.organization_types)
        self.assertIn({'name': 'Regiment', 'token': 'regiment'},
                      mydirectory.organization_levels)

    def test_person(self):
        self.assertIn('degaulle', self.mydirectory)
        degaulle = self.degaulle
        #self.assertEqual('Charles De Gaulle', degaulle.Title())
        self.assertEqual('De Gaulle', degaulle.lastname)
        self.assertEqual('Charles', degaulle.firstname)
        self.assertEqual(datetime.date(1890, 11, 22), degaulle.birthday)
        with self.assertRaises(ValueError):
            self.portal.invokeFactory('person', 'error',
                                      {'lastname': "Toto"})

    def test_organization(self):
        self.assertIn('armeedeterre', self.mydirectory)
        armeedeterre = self.mydirectory['armeedeterre']
        self.assertIn('corpsa', armeedeterre)
        self.assertIn('corpsb', armeedeterre)
        self.assertIn('divisionalpha', armeedeterre['corpsa'])
        #self.assertIn('divisionalpha', armeedeterre)
        divisionalpha = armeedeterre['corpsa']['divisionalpha']
        self.assertIn('armeedeterre', divisionalpha.getPhysicalPath())

    def test_position(self):
        self.assertIn('general_adt', self.armeedeterre)

    def test_held_position(self):
        degaulle = self.degaulle
        self.assertIn('adt', degaulle)
        self.assertIn('gadt', degaulle)

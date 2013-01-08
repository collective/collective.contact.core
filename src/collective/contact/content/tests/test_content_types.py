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
        self.pepper = self.mydirectory['pepper']
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
        self.assertEqual('Général Charles De Gaulle', degaulle.Title())
        self.assertEqual('De Gaulle', degaulle.lastname)
        self.assertEqual('Charles', degaulle.firstname)
        self.assertEqual(datetime.date(1890, 11, 22), degaulle.birthday)
        with self.assertRaises(ValueError):
            self.portal.invokeFactory('person', 'error',
                                      {'lastname': "Toto"})

    def test_organization(self):
        self.assertIn('armeedeterre', self.mydirectory)
        armeedeterre = self.mydirectory['armeedeterre']
        self.assertEqual(armeedeterre.Title(), "Armée de terre")
        self.assertIn('Armée de terre', armeedeterre.get_full_title())
        self.assertIn('corpsa', armeedeterre)
        corpsa = armeedeterre['corpsa']
        self.assertIn('corpsb', armeedeterre)
        self.assertIn('divisionalpha', corpsa)
        divisionalpha = corpsa['divisionalpha']
        self.assertIn('divisionbeta', corpsa)
        self.assertIn('regimenth', divisionalpha)
        regimenth = divisionalpha['regimenth']
        self.assertIn('brigadelh', regimenth)
        brigadelh = regimenth['brigadelh']

        corpsa_full_title = corpsa.get_full_title()
        self.assertIn('Armée de terre', corpsa_full_title)
        self.assertIn('Corps A', corpsa_full_title)

        division_alpha_full_title = divisionalpha.get_full_title()
        self.assertIn('armeedeterre', divisionalpha.getPhysicalPath())
        self.assertIn('Armée de terre', division_alpha_full_title)
        self.assertIn('Corps A', division_alpha_full_title)
        self.assertIn('Division Alpha', division_alpha_full_title)

        brigadelh_full_title = brigadelh.get_full_title()
        self.assertIn('armeedeterre', brigadelh.getPhysicalPath())
        self.assertIn('Armée de terre', brigadelh_full_title)
        self.assertIn('Corps A', brigadelh_full_title)
        self.assertIn('Division Alpha', brigadelh_full_title)
        self.assertIn('Régiment H', brigadelh_full_title)
        self.assertIn('Brigade LH', brigadelh_full_title)

    def test_position(self):
        self.assertIn('general_adt', self.armeedeterre)
        general_adt = self.general_adt
        self.assertEqual(general_adt.Title(),
                         "Général de l'armée de terre")
        self.assertEqual(general_adt.position_type,
                         'general')

    def test_held_position(self):
        degaulle = self.degaulle
        self.assertIn('adt', degaulle)
        self.assertIn('gadt', degaulle)
        pepper = self.pepper
        self.assertIn('sergent_pepper', pepper)

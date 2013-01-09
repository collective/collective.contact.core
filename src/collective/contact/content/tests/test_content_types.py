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
        mydirectory = self.mydirectory
        self.assertIn('degaulle', mydirectory)
        degaulle = self.degaulle
        self.assertEqual('Général Charles De Gaulle', degaulle.Title())
        self.assertEqual('De Gaulle', degaulle.lastname)
        self.assertEqual('Charles', degaulle.firstname)
        self.assertEqual(datetime.date(1890, 11, 22), degaulle.birthday)
        pepper = mydirectory['pepper']
        self.assertEqual('Sergent Pepper', pepper.Title())
        rambo = mydirectory['rambo']
        self.assertEqual('John Rambo', rambo.Title())
        # we can't create persons in portal
        with self.assertRaises(ValueError):
            self.portal.invokeFactory('person', 'error',
                                      {'lastname': "Casper"})

    def test_organization(self):
        self.assertIn('armeedeterre', self.mydirectory)
        armeedeterre = self.mydirectory['armeedeterre']
        self.assertEqual(armeedeterre.Title(), "Armée de terre")
        self.assertIn('Armée de terre', armeedeterre.get_organizations_titles())
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

        corpsa_titles = corpsa.get_organizations_titles()
        self.assertIn('Armée de terre', corpsa_titles)
        self.assertIn('Corps A', corpsa_titles)

        division_alpha_titles = divisionalpha.get_organizations_titles()
        self.assertIn('armeedeterre', divisionalpha.getPhysicalPath())
        self.assertIn('Armée de terre', division_alpha_titles)
        self.assertIn('Corps A', division_alpha_titles)
        self.assertIn('Division Alpha', division_alpha_titles)

        brigadelh_titles = brigadelh.get_organizations_titles()
        self.assertIn('armeedeterre', brigadelh.getPhysicalPath())
        self.assertIn('Armée de terre', brigadelh_titles)
        self.assertIn('Corps A', brigadelh_titles)
        self.assertIn('Division Alpha', brigadelh_titles)
        self.assertIn('Régiment H', brigadelh_titles)
        self.assertIn('Brigade LH', brigadelh_titles)
        self.assertEqual(brigadelh.get_full_title(),
                         "Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH")

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
        adt = degaulle['adt']
        self.assertEqual(adt.Title(),
                         "Armée de terre")
        self.assertEqual(adt.get_full_title(),
                         "Général Charles De Gaulle (Armée de terre)")
        self.assertIn('gadt', degaulle)
        gadt = degaulle['gadt']
        self.assertEqual(gadt.Title(),
                         "Général de l'armée de terre")
        self.assertEqual(gadt.get_full_title(),
                         "Général Charles De Gaulle (Armée de terre - Général de l'armée de terre)")
        pepper = self.pepper
        self.assertIn('sergent_pepper', pepper)
        sergent_pepper = pepper['sergent_pepper']
        self.assertEqual(sergent_pepper.Title(),
                         "Sergent de la brigade LH")
        self.assertEqual(sergent_pepper.get_full_title(),
                         "Sergent Pepper (Armée de terre - Sergent de la brigade LH)")

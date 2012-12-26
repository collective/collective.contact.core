# -*- coding: utf8 -*-

import unittest2 as unittest

from DateTime import DateTime

from ecreall.helpers.testing.base import BaseTest

######### from Products.CMFCore.utils import getToolByName

from collective.contact.content.testing import INTEGRATION


class TestContentTypes(unittest.TestCase, BaseTest):
    """Tests new content types"""

    layer = INTEGRATION

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.portal = self.layer['portal']
        self.login('manager')

        position_types = [{'Name': 'General', 'Token': 'general'},
                          {'Name': 'Sergeant', 'Token': 'sergeant'},
                          {'Name': 'Colonel', 'Token': 'colonel'},
                          {'Name': 'Lieutenant', 'Token': 'lieutenant'},
                          {'Name': 'Captain', 'Token': 'captain'},
                          {'Name': 'Admiral', 'Token': 'admiral'},
                          ]

        organization_types = [{'Name': 'Navy', 'Token': 'navy'},
                              {'Name': 'Army', 'Token': 'army'},
                              {'Name': 'Air force', 'Token': 'air_force'},
                              ]

        organization_levels = [{'Name': 'Corps', 'Token': 'corps'},
                               {'Name': 'Division', 'Token': 'division'},
                               {'Name': 'Brigade', 'Token': 'brigade'},
                               {'Name': 'Regiment', 'Token': 'regiment'},
                               {'Name': 'Squad', 'Token': 'squad'},
                               ]

        params = {'title': "Military directory",
                  'position_types': position_types,
                  'organization_types': organization_types,
                  'organization_levels': organization_levels,
                  }
        self.portal.invokeFactory('directory', 'mydirectory', **params)
        mydirectory = self.portal['mydirectory']

        params = {'lastname': 'De Gaulle',
                  'firstname': 'Charles',
                  'gender': 'M',
                  'person_title': u'Général',
                  'birthday': DateTime('1890-11-22'),
                  'email': 'charles.de.gaulle@armees.fr',
                  }
        mydirectory.invokeFactory('person', 'degaulle', **params)

        params = {'title': "Armée de terre",
                  'organization_type': 'army',
                  }
        mydirectory.invokeFactory('organization', 'armeedeterre', **params)
        armeedeterre = mydirectory['armeedeterre']

        params = {'title': "Corps A",
                  'organization_type': 'corps',
                  }
        armeedeterre.invokeFactory('organization', 'corpsa', **params)
        corpsa = armeedeterre['corpsa']

        params = {'title': "Corps B",
                  'organization_type': 'corps',
                  }
        armeedeterre.invokeFactory('organization', 'corpsb', **params)

        params = {'title': "Division Alpha",
                  'organization_type': 'division',
                  }
        corpsa.invokeFactory('organization', 'divisionalpha', **params)

        params = {'title': u"General of armée de terre",
                  'position_type': 'general',
                  }
        armeedeterre.invokeFactory('position', 'general_adt', **params)

        self.mydirectory = mydirectory
        self.degaulle = mydirectory['degaulle']
        self.armeedeterre = armeedeterre
        self.general_adt = armeedeterre['general_adt']

    def test_directory(self):
        self.assertIn('mydirectory', self.portal)
        mydirectory = self.portal['mydirectory']
        self.assertEqual('Military directory', mydirectory.Title())
        self.assertIn({'Name': 'Colonel', 'Token': 'colonel'},
                      mydirectory.position_types)
        self.assertIn({'Name': 'Air force', 'Token': 'air_force'},
                      mydirectory.organization_types)
        self.assertIn({'Name': 'Regiment', 'Token': 'regiment'},
                      mydirectory.organization_levels)

    def test_person(self):
        self.assertIn('degaulle', self.mydirectory)
        degaulle = self.degaulle
        #self.assertEqual('Charles De Gaulle', degaulle.Title())
        self.assertEqual('De Gaulle', degaulle.lastname)
        self.assertEqual('Charles', degaulle.firstname)
        self.assertEqual(DateTime('1890-11-22'), degaulle.birthday)
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
        armeedeterre = self.armeedeterre
        params = {'start_date': DateTime('1940-05-25'),
                  'end_date': DateTime('1970-11-09'),
                  'position': armeedeterre,
                  }
        degaulle.invokeFactory('held_position', 'adt', **params)
        self.assertIn('adt', degaulle)

        general_adt = self.general_adt
        params = {'start_date': DateTime('1940-05-25'),
                  'end_date': DateTime('1970-11-09'),
                  'position': general_adt,
                  }
        degaulle.invokeFactory('held_position', 'gadt', **params)
        self.assertIn('gadt', degaulle)

# -*- coding: utf8 -*-

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.utils import get_gender_and_number
from collective.contact.core.utils import get_position_type_name
from ecreall.helpers.testing.base import BaseTest
from plone.app.testing.interfaces import TEST_USER_NAME

import unittest


class TestUtils(unittest.TestCase, BaseTest):

    layer = INTEGRATION

    def setUp(self):
        super(TestUtils, self).setUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        mydirectory = self.portal['mydirectory']
        self.degaulle = mydirectory['degaulle']
        self.pepper = mydirectory['pepper']
        self.sergent_pepper = self.pepper['sergent_pepper']
        self.draper = mydirectory['draper']
        self.rambo = mydirectory['rambo']
        self.armeedeterre = mydirectory['armeedeterre']
        self.captain_crunch = self.draper['captain_crunch']
        self.mydirectory = mydirectory

    def test_get_gender_and_number(self):
        """ """
        self.login(TEST_USER_NAME)

        # if only non genderable contacts, returns None
        self.assertIsNone(get_gender_and_number([]))
        self.assertIsNone(get_gender_and_number([self.armeedeterre]))

        # possible to pass mix of different types of contact
        self.assertEqual(
            get_gender_and_number([self.armeedeterre, self.sergent_pepper]), u'MS')
        self.assertEqual(
            get_gender_and_number([self.degaulle, self.sergent_pepper]), u'MP')

        # Male, Singular
        self.assertEqual(
            get_gender_and_number([self.sergent_pepper]), u'MS')
        # Male, Plural
        self.assertEqual(
            get_gender_and_number([self.sergent_pepper, self.degaulle]), u'MP')

        # change gender to have females
        self.rambo.gender = u'F'
        self.draper.gender = u'F'
        # Female, Singular
        self.assertEqual(
            get_gender_and_number([self.rambo]), u'FS')
        # Female, Plural
        self.assertEqual(
            get_gender_and_number([self.rambo, self.draper]), u'FP')

        # Male have priority over Female
        # Male, Plural
        self.assertEqual(get_gender_and_number([self.sergent_pepper, self.draper]), u'MP')

        # user unicity, if we pass twice same person, it stays singular, even thru held_position
        self.assertEqual(get_gender_and_number([self.pepper, self.sergent_pepper]), u'MS')

        # parameters use_by and use_to will prepend a 'B' or 'T' to returned value
        self.assertEqual(get_gender_and_number([self.sergent_pepper, self.draper], use_by=True), u'BMP')
        self.assertEqual(get_gender_and_number([self.pepper, self.sergent_pepper], use_to=True), u'TMS')

    def test_get_position_type_name(self):
        """ """
        self.login(TEST_USER_NAME)
        self.assertIsNone(get_position_type_name(self.mydirectory, ''))
        self.assertIsNone(get_position_type_name(self.mydirectory, None))
        self.assertEqual(get_position_type_name(self.mydirectory, 'general'), u'General')
        self.assertEqual(get_position_type_name(self.mydirectory, 'captain'), u'Captain')

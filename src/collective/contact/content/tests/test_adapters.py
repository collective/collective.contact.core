# -*- coding: utf8 -*-

import unittest2 as unittest

from ecreall.helpers.testing.base import BaseTest

from collective.contact.content.testing import INTEGRATION
from collective.contact.vcard.interfaces import IVCard


class TestAdapters(unittest.TestCase, BaseTest):
    """Tests adapters"""

    layer = INTEGRATION

    def setUp(self):
        super(TestAdapters, self).setUp()
        self.portal = self.layer['portal']
        self.directory = self.portal['mydirectory']
        self.degaulle = self.directory['degaulle']

    def test_held_position_vcard(self):
        gadt = self.degaulle['gadt']
        vcard_provider = IVCard(gadt)
        vcard = vcard_provider.get_vcard()
        self.assertEqual(vcard.fn.value, 'Charles De Gaulle')
        self.assertEqual(vcard.org.value, 'Armée de terre')
        self.assertEqual(vcard.role.value, 'General of armée de terre')
        self.assertEqual(vcard.title.value, 'General of armée de terre')
        self.assertEqual(vcard.email.value, 'charles.de.gaulle@armees.fr')
        self.assertEqual(vcard.email.type_param, 'INTERNET')
        self.assertFalse(hasattr(vcard, 'adr'))
        self.assertFalse(hasattr(vcard, 'tel_list'))
        self.assertEqual(vcard.bday.value, '1890-11-22')

# -*- coding: utf8 -*-

import unittest2 as unittest

from ecreall.helpers.testing.base import BaseTest

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.interfaces import IVCard


class TestAdapters(unittest.TestCase, BaseTest):
    """Tests adapters"""

    layer = INTEGRATION

    def setUp(self):
        super(TestAdapters, self).setUp()
        self.portal = self.layer['portal']
        self.directory = self.portal['mydirectory']
        self.degaulle = self.directory['degaulle']
        self.pepper = self.directory['pepper']

    def test_gadt_vcard(self):
        gadt = self.degaulle['gadt']
        vcard_provider = IVCard(gadt)
        vcard = vcard_provider.get_vcard()
        self.assertEqual(vcard.fn.value, u'Charles De Gaulle')
        self.assertEqual(vcard.org.value, [u'Armée de terre'])
        self.assertEqual(vcard.role.value, u"Général de l'armée de terre")
        self.assertEqual(vcard.title.value, u"Général de l'armée de terre")
        self.assertEqual(vcard.email.value, 'charles.de.gaulle@armees.fr')
        self.assertEqual(vcard.email.type_param, 'INTERNET')
        self.assertTrue(hasattr(vcard, 'adr'))
        self.assertFalse(hasattr(vcard, 'tel_list'))
        self.assertEqual(vcard.bday.value, '1901-11-22')

    def test_sgt_pepper_vcard(self):
        sergent_pepper = self.pepper['sergent_pepper']
        vcard_provider = IVCard(sergent_pepper)
        vcard = vcard_provider.get_vcard()
        self.assertEqual(vcard.fn.value, 'Pepper')
        self.assertEqual(vcard.org.value,
                         [u'Armée de terre', u'Corps A', u'Division Alpha',
                          u'Régiment H', u'Brigade LH'])
        self.assertEqual(vcard.role.value, "Sergent de la brigade LH")

        # TODO: test a held_position without address ?? Rambo ? (associate new Organization and Position to Rambo)
        # self.assertFalse(hasattr(vcard, 'adr'))

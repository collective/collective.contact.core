# -*- coding: utf8 -*-
import unittest2 as unittest

from collective.contact.content.testing import INTEGRATION


ADDRESS_FIELDS = ['country', 'region', 'zip_code',
                  'city', 'street', 'number',
                  'additional_address_details']


class TestView(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        super(TestView, self).setUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        mydirectory = self.portal['mydirectory']
        self.degaulle = mydirectory['degaulle']
        self.adt = self.degaulle['adt']
        self.gadt = self.degaulle['gadt']
        self.pepper = mydirectory['pepper']
        self.sergent_pepper = self.pepper['sergent_pepper']
        self.rambo = mydirectory['rambo']
        self.regimenth = mydirectory['armeedeterre']['corpsa']['divisionalpha']['regimenth']
        self.mydirectory = mydirectory


class TestAddressView(TestView):

    def test_degaulle_address_view(self):
        address_view = self.degaulle.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['country'], 'France')
        self.assertEqual(data['number'], '6bis')
        self.assertEqual(data['street'], 'rue Jean Moulin')
        self.assertEqual(data['city'], "Colombey les deux églises")
        self.assertEqual(data['zip_code'], '52330')
        self.assertEqual(data['region'], '')
        self.assertEqual(data['additional_address_details'], 'bâtiment D')

    def test_pepper_address_view(self):
        address_view = self.pepper.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['country'], 'England')
        self.assertEqual(data['city'], "Liverpool")

    def test_rambo_address_view(self):
        # no address information
        address_view = self.rambo.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
            self.assertEqual(data[field], '')

    def test_regimenth_address_view(self):
        # an organization have an address view
        address_view = self.regimenth.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['number'], '11')
        self.assertEqual(data['street'], "rue de l'harmonie")
        self.assertEqual(data['city'], "Villeneuve d'Ascq")
        self.assertEqual(data['zip_code'], '59650')
        self.assertEqual(data['region'], '')
        self.assertEqual(data['additional_address_details'], '')
    # TODO: test that a position can have an address


class TestContactView(TestView):

    def test_contact_view(self):
        contact_view = self.gadt.restrictedTraverse("@@contact")
        contact_view.update()

        self.assertEqual(contact_view.fullname,
                         "Général Charles De Gaulle")
        organizations_names = contact_view.organizations_names
        self.assertEqual(['Armée de terre'],
                         organizations_names)
        # address is acquired from degaulle
        address = contact_view.address
        self.assertEqual(address['number'], '6bis')
        self.assertEqual(address['street'], "rue Jean Moulin")
        self.assertEqual(address['city'], "Colombey les deux églises")
        self.assertEqual(address['zip_code'], '52330')
        self.assertEqual(address['region'], '')
        self.assertEqual(address['additional_address_details'], 'bâtiment D')

    def test_contact_details_acquisition(self):
        contact_view = self.sergent_pepper.restrictedTraverse("@@contact")
        contact_view.update()
        self.assertEqual(contact_view.fullname, "Sergent Pepper")
        organizations_names = contact_view.organizations_names
        self.assertEqual(['Armée de terre', 'Corps A',
                          'Division Alpha', 'Régiment H',
                          'Brigade LH'], organizations_names)

        # Person email comes before Position email
        self.assertEqual(contact_view.email,
                         "sgt.pepper@armees.fr")
        self.assertNotEqual(contact_view.email,
                            "brigade_lh@armees.fr")
        self.assertEqual(contact_view.phone,
                         "0288552211")
        self.assertEqual(contact_view.cell_phone,
                         '0654875233')
        self.assertEqual(contact_view.im_handle,
                         "brigade_lh@jabber.org")

        # Everything in Sgt Pepper's address is acquired from Régiment H
        address = contact_view.address
        self.assertEqual(address['number'], '11')
        self.assertEqual(address['street'], "rue de l'harmonie")
        self.assertEqual(address['city'], "Villeneuve d'Ascq")
        self.assertEqual(address['zip_code'], '59650')
        self.assertEqual(address['region'], '')
        self.assertEqual(address['additional_address_details'], '')

# -*- coding: utf8 -*-
import unittest2 as unittest

from plone.app.testing.interfaces import TEST_USER_NAME

from ecreall.helpers.testing.base import BaseTest

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.behaviors import ADDRESS_FIELDS


class TestView(unittest.TestCase, BaseTest):

    layer = INTEGRATION

    def setUp(self):
        super(TestView, self).setUp()
        self.login(TEST_USER_NAME)
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        mydirectory = self.portal['mydirectory']
        self.degaulle = mydirectory['degaulle']
        self.adt = self.degaulle['adt']
        self.gadt = self.degaulle['gadt']
        self.pepper = mydirectory['pepper']
        self.sergent_pepper = self.pepper['sergent_pepper']
        self.rambo = mydirectory['rambo']
        self.armeedeterre = mydirectory['armeedeterre']
        self.corpsa = self.armeedeterre['corpsa']
        self.divisionalpha = self.corpsa['divisionalpha']
        self.regimenth = self.divisionalpha['regimenth']
        self.brigadelh = self.regimenth['brigadelh']
        self.general_adt = self.armeedeterre['general_adt']
        self.sergent_lh = self.brigadelh['sergent_lh']
        self.draper = mydirectory['draper']
        self.captain_crunch = self.draper['captain_crunch']
        self.mydirectory = mydirectory


class TestAddressView(TestView):

    def test_degaulle_address_view(self):
        address_view = self.degaulle.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['country'], u'France')
        self.assertEqual(data['number'], u'6bis')
        self.assertEqual(data['street'], u'rue Jean Moulin')
        self.assertEqual(data['city'], u"Colombey les deux églises")
        self.assertEqual(data['zip_code'], u'52330')
        self.assertEqual(data['region'], u'')
        self.assertEqual(data['additional_address_details'], u'bâtiment D')

    def test_pepper_address_view(self):
        address_view = self.pepper.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['country'], u'England')
        self.assertEqual(data['city'], u"Liverpool")

    def test_rambo_address_view(self):
        # no address information
        address_view = self.rambo.restrictedTraverse("@@address")
        data = address_view.namespace()
        self.assertEqual(data, {})

    def test_regimenth_address_view(self):
        # an organization have an address view
        address_view = self.regimenth.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data['number'], u'11')
        self.assertEqual(data['street'], u"rue de l'harmonie")
        self.assertEqual(data['city'], u"Villeneuve d'Ascq")
        self.assertEqual(data['zip_code'], u'59650')
        self.assertEqual(data['region'], u'')
        self.assertEqual(data['additional_address_details'], u'')


class TestContactView(TestView):

    def xtest_contact_view(self):
        view = self.gadt.restrictedTraverse("view")
        view.update()

        self.assertEqual(view.fullname,
                         "Général Charles De Gaulle")
        self.assertEqual([self.armeedeterre], view.organizations)
        self.assertEqual(view.birthday, 'Nov 22, 1901')

        # address is acquired from degaulle
        address = view.address
        self.assertEqual(address['number'], u'6bis')
        self.assertEqual(address['street'], u"rue Jean Moulin")
        self.assertEqual(address['city'], u"Colombey les deux églises")
        self.assertEqual(address['zip_code'], u'52330')
        self.assertEqual(address['region'], u'')
        self.assertEqual(address['additional_address_details'], u'bâtiment D')

    def xtest_empty_fields(self):
        view = self.captain_crunch.restrictedTraverse("view")
        view.update()
        self.assertEqual(view.start_date, u'')
        self.assertEqual(view.end_date, u'')
        self.assertEqual(view.birthday, u'')
        self.assertEqual(view.gender, u'')
        self.assertEqual(view.photo, u'')

    def xtest_contact_details_acquisition(self):
        view = self.sergent_pepper.restrictedTraverse("view")
        view.update()
        self.assertEqual(view.fullname, "Sergent Pepper")
        self.assertEqual(self.sergent_lh,
                         view.position)
        organizations = view.organizations
        self.assertEqual([self.armeedeterre,
                          self.corpsa,
                          self.divisionalpha,
                          self.regimenth,
                          self.brigadelh], organizations)

        # Person email comes before Position email
        self.assertEqual(view.contact_details['email'],
                         "sgt.pepper@armees.fr")
        self.assertEqual(view.contact_details['phone'],
                         "0288552211")
        self.assertEqual(view.contact_details['cell_phone'],
                         '0654875233')
        self.assertEqual(view.contact_details['im_handle'],
                         "brigade_lh@jabber.org")

        # Everything in Sgt Pepper's address is acquired from Régiment H
        address = view.contact_details['address']
        self.assertEqual(address['number'], u'11')
        self.assertEqual(address['street'], u"rue de l'harmonie")
        self.assertEqual(address['city'], u"Villeneuve d'Ascq")
        self.assertEqual(address['zip_code'], u'59650')
        self.assertEqual(address['region'], u'')
        self.assertEqual(address['additional_address_details'], u'')


class TestPositionView(TestView):

    def test_position_basefields_view(self):
        view = self.sergent_lh.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(view.name, u"Sergent de la brigade LH, Brigade LH (Armée de terre)")
        self.assertEqual(view.type, "Sergeant")

    def test_position_view(self):
        view = self.sergent_lh.restrictedTraverse("view")
        view.update()
        organizations = view.organizations
        self.assertEqual([self.armeedeterre,
                          self.corpsa,
                          self.divisionalpha,
                          self.regimenth,
                          self.brigadelh], organizations)

    def test_position_contact_details_view(self):
        view = self.sergent_lh.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details['email'],
                         "brigade_lh@armees.fr")

        address = view.contact_details['address']
        self.assertEqual(address['number'], u'11')
        self.assertEqual(address['street'], u"rue de l'harmonie")
        self.assertEqual(address['city'], u"Villeneuve d'Ascq")
        self.assertEqual(address['zip_code'], u'59650')
        self.assertEqual(address['region'], u'')
        self.assertEqual(address['additional_address_details'], u'')


class TestOrganizationView(TestView):

    def test_organization_basefields_view(self):
        view = self.corpsa.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(view.name, "Corps A")
        self.assertEqual(view.type, "Corps")

    def test_organization_view(self):
        view = self.corpsa.restrictedTraverse("view")
        view.update()
        parent_organizations = view.parent_organizations
        self.assertEqual([self.armeedeterre], parent_organizations)

    def test_organization_contact_details_view(self):
        view = self.corpsa.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details['email'], '')

        address = view.contact_details['address']
        self.assertEqual(address['number'], u'')
        self.assertEqual(address['street'], u"rue Philibert Lucot")
        self.assertEqual(address['city'], u'Orléans')
        self.assertEqual(address['zip_code'], u'')
        self.assertEqual(address['region'], u'')
        self.assertEqual(address['country'], u'France')
        self.assertEqual(address['additional_address_details'], u'')

    def test_sub_organizations(self):
        view = self.armeedeterre.restrictedTraverse("view")
        view.update()
        sub_organizations_names = [e.Title for e in view.sub_organizations]
        self.assertEqual(set(['Corps A', 'Corps B']),
                         set(sub_organizations_names))
        # no sub-organizations
        view = self.brigadelh.restrictedTraverse("view")
        view.update()
        self.assertEqual(0, len(view.sub_organizations))

    def test_positions(self):
        view = self.armeedeterre.restrictedTraverse("view")
        view.update()
        positions_names = [e.Title() for e in view.positions]
        self.assertEqual(set(["Général de l'armée de terre"]),
                         set(positions_names))
        # no_positions
        view = self.corpsa.restrictedTraverse("view")
        view.update()
        self.assertEqual(0, len(view.positions))

    def test_othercontacts(self):
        view = self.armeedeterre.restrictedTraverse("@@othercontacts")
        view.update()
        contact = view.othercontacts[0]
        self.assertEqual(contact['title'], 'Général Charles De Gaulle')
        self.assertEqual(contact['held_position'], 'Armée de terre')
        self.assertIsNone(contact['label'])
        self.assertEqual(contact['obj'], self.adt)
        self.assertEqual(contact['email'], u'charles.de.gaulle@armees.fr')
        self.assertIsNone(contact['phone'])
        self.assertIsNone(contact['cell_phone'])
        self.assertIsNone(contact['fax'])
        self.assertIsNone(contact['im_handle'])
        self.assertEqual(contact['website'], 'http://www.charles-de-gaulle.org')


class TestPersonView(TestView):

    def test_person_basefields_view(self):
        view = self.degaulle.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(view.name, "Général Charles De Gaulle")
        self.assertEqual(view.gender, 'M')
        self.assertIn(view.birthday, ('Nov 22, 1901', '1901-11-22'))

    def test_person_contact_details_view(self):
        view = self.degaulle.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details['email'], 'charles.de.gaulle@armees.fr')
        self.assertEqual(view.contact_details['phone'], '')
        self.assertEqual(view.contact_details['cell_phone'], '')
        self.assertEqual(view.contact_details['im_handle'], '')

        address = view.contact_details['address']
        self.assertEqual(address['number'], u'6bis')
        self.assertEqual(address['street'], u"rue Jean Moulin")
        self.assertEqual(address['city'], u'Colombey les deux églises')
        self.assertEqual(address['zip_code'], u'52330')
        self.assertEqual(address['region'], u'')
        self.assertEqual(address['country'], u'France')
        self.assertEqual(address['additional_address_details'], u'bâtiment D')

    def test_person_held_positions_view(self):
        view = self.degaulle.restrictedTraverse("@@heldpositions")
        view.update()
        held_positions = view.held_positions
        self.assertEqual(len(held_positions), 2)

        first = held_positions[0]
        self.assertEqual(self.adt, first['object'])
        self.assertEqual(self.adt.Title(), first['label'])
        self.assertIn(first['start_date'], [u'May 25, 1940', '1940-05-25'])
        self.assertEqual(self.armeedeterre, first['organization'])

        second = held_positions[1]
        self.assertEqual(self.gadt, second['object'])
        self.assertEqual(self.gadt.label, second['label'])
        self.assertIn(second['start_date'], [u'May 25, 1940', '1940-05-25'])
        self.assertIn(second['end_date'], [u'Nov 09, 1970', '1970-11-09'])
        self.assertEqual(self.armeedeterre, second['organization'])

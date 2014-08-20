# -*- coding: utf8 -*-
import datetime
import unittest2 as unittest

from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from plone import api
from plone.app.testing.interfaces import TEST_USER_NAME
from z3c.relationfield.relation import RelationValue

from ecreall.helpers.testing.base import BaseTest

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.interfaces import IVCard, IPersonHeldPositions,\
    IContactable


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

    def test_regimenth_vcard(self):
        regimenth = self.directory['armeedeterre']['corpsa']['divisionalpha']['regimenth']
        vcard_provider = IVCard(regimenth)
        vcard = vcard_provider.get_vcard()
        self.assertEqual(vcard.fn.value, u'Régiment H'.encode('utf-8'))
        self.assertEqual(vcard.kind.value, 'org')
        self.assertTrue(hasattr(vcard, 'adr'))

    def test_person_held_positions(self):
        self.login(TEST_USER_NAME)
        degaulle = self.directory.degaulle
        intids = getUtility(IIntIds)
        # de gaulle in 1960...
        api.content.create(container=self.directory, type='organization', id='france',
                           )
        api.content.create(container=degaulle, type='held_position', id='president',
                           start_date=datetime.date(1959, 1, 8),
                           position=RelationValue(intids.getId(self.directory.france)))
        api.content.create(container=degaulle, type='held_position', id='lieutenant-colonel',
                           position=RelationValue(intids.getId(self.directory.armeedeterre)),
                           end_date=datetime.date(1940, 6, 1),
                           start_date=datetime.date(1933, 12, 25))
        api.content.create(container=degaulle, type='held_position', id='commandant',
                           position=RelationValue(intids.getId(self.directory.armeedeterre)),
                           start_date=datetime.date(1927, 10, 9),
                           end_date=datetime.date(1933, 12, 25))
        del self.degaulle.gadt.end_date
        self.degaulle.moveObjectsToTop(['president'])

        adapter = IPersonHeldPositions(degaulle)
        self.assertEqual(adapter.get_main_position(), self.degaulle.president)
        self.assertEqual(adapter.get_current_positions(),
                         (self.degaulle.president,
                          self.degaulle.gadt, ))
        self.assertEqual(adapter.get_sorted_positions(),
                         (self.degaulle.president,
                          self.degaulle.gadt,
                          degaulle.adt,
                          degaulle['lieutenant-colonel'],
                          self.degaulle['commandant'],
                          ))

        api.content.transition(degaulle.adt, 'deactivate')
        self.assertEqual(adapter.get_main_position(), self.degaulle.president)

        api.content.transition(degaulle.president, 'deactivate')
        self.assertEqual(adapter.get_main_position(), degaulle.gadt)

    def test_contact_details(self):
        details = IContactable(self.degaulle).get_contact_details()
        self.assertEqual(details['website'], 'http://www.charles-de-gaulle.org')
        self.assertEqual(details['email'], 'charles.de.gaulle@armees.fr')
        self.assertEqual(details['address'], {'city': u'Colombey les deux \xe9glises',
                                              'country': u'France', 'region': '',
                                              'additional_address_details': u'b\xe2timent D',
                                              'number': u'6bis',
                                              'street': u'rue Jean Moulin',
                                              'zip_code': u'52330'})

        details = IContactable(self.degaulle).get_contact_details(keys=('email',))
        self.assertEqual(details, {'email': 'charles.de.gaulle@armees.fr'})

        details = IContactable(self.pepper).get_contact_details()
        self.assertEqual(details['website'], 'http://www.sergent-pepper.org')

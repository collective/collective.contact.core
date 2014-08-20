# -*- coding: utf8 -*-
import unittest2 as unittest

from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from plone.behavior.interfaces import IBehavior
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.testing.helpers import setRoles
from plone.app.testing.interfaces import TEST_USER_NAME, TEST_USER_ID

from ecreall.helpers.testing.base import BaseTest

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.behaviors import IContactDetails,\
    IGlobalPositioning, IBirthday


class TestBehaviors(unittest.TestCase, BaseTest):
    """Tests behaviors"""

    layer = INTEGRATION

    def setUp(self):
        super(TestBehaviors, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.login(TEST_USER_NAME)
        self.portal.invokeFactory('testtype', 'testitem')
        self.testitem = self.portal['testitem']

    def test_behaviors_installation(self):
        contact_details_behavior = getUtility(IBehavior,
                name='collective.contact.core.behaviors.IContactDetails')
        global_positioning_behavior = getUtility(IBehavior,
                name='collective.contact.core.behaviors.IGlobalPositioning')
        birthday_behavior = getUtility(IBehavior,
                name='collective.contact.core.behaviors.IBirthday')
        self.assertEqual(contact_details_behavior.interface, IContactDetails)
        self.assertEqual(global_positioning_behavior.interface,
                         IGlobalPositioning)
        self.assertEqual(birthday_behavior.interface, IBirthday)
        IFormFieldProvider.providedBy(contact_details_behavior.interface)
        IFormFieldProvider.providedBy(global_positioning_behavior.interface)
        IFormFieldProvider.providedBy(birthday_behavior.interface)

    def test_contact_details_fields(self):
        item = self.testitem
        self.assertIsNone(item.getAttributes())
        for attr in ('country', 'region', 'zip_code', 'city', 'street',
                     'number', 'im_handle', 'cell_phone', 'phone', 'email',
                     'fax', 'website',
                     'additional_address_details', 'birthday'):
            self.assertTrue(hasattr(item, attr))
        item.phone = '0655443322'
        item.email = 'toto@example.com'
        item.zip_code = '59650'
        self.assertEqual(item.phone, '0655443322')
        self.assertEqual(item.email, 'toto@example.com')
        self.assertEqual(item.zip_code, '59650')

        # test clear values when use_parent_address is selected
        item.use_parent_address = True
        notify(ObjectModifiedEvent(item))
        self.assertEqual(item.zip_code, None)
        self.assertEqual(item.phone, '0655443322')

    def test_global_positioning_fields(self):
        item = self.testitem
        item.latitude = 45.2
        item.longitude = -23.8
        self.assertEqual(item.latitude, 45.2)
        self.assertEqual(item.longitude, -23.8)

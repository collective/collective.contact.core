# -*- coding: utf8 -*-

import unittest2 as unittest

from Products.CMFDefault.Document import Document

from plone.app.testing.interfaces import TEST_USER_NAME, TEST_USER_ID

from ecreall.helpers.testing.base import BaseTest

from collective.contact.content.testing import INTEGRATION
from collective.contact.content.behaviors import IContactDetails,\
    IGlobalPositioning


from StringIO import StringIO
from zope.configuration import xmlconfig
from plone.behavior.interfaces import IBehaviorAssignable
from zope.component import adapts
from zope.component import provideAdapter
from zope.interface import implements
from zope.component import getUtility
from plone.behavior.interfaces import IBehavior
from plone.autoform.interfaces import IFormFieldProvider
from zope.component._api import queryUtility
from collective.contact.content.position import Position
from plone.app.testing.helpers import setRoles


configuration = """\
    <configure
        xmlns="http://namespaces.zope.org/zope"
        i18n_domain="collective.contact.content">

        <include package="five.grok" />
        <include package="Products.Five" file="meta.zcml" />
        <include package="collective.contact.content" file="behaviors.zcml" />
    </configure>
"""

xmlconfig.xmlconfig(StringIO(configuration))

class TestingAssignable(object):
    implements(IBehaviorAssignable)
    adapts(Document)
    enabled = [IContactDetails, IGlobalPositioning]

    def __init__(self, context):
        self.context = context

    def supports(self, behavior_interface):
        return behavior_interface in self.enabled

    def enumerate_behaviors(self):
        for e in self.enabled:
            yield queryUtility(IBehavior, name=e.__identifier__)

provideAdapter(TestingAssignable)


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
                                              name='collective.contact.content.behaviors.IContactDetails')
        global_positioning_behavior = getUtility(IBehavior,
                                      name='collective.contact.content.behaviors.IGlobalPositioning')
        self.assertEqual(contact_details_behavior.interface, IContactDetails)
        self.assertEqual(global_positioning_behavior.interface, IGlobalPositioning)
        IFormFieldProvider.providedBy(contact_details_behavior.interface)
        IFormFieldProvider.providedBy(global_positioning_behavior.interface)

### TODO: these tests don't work as expected, see doc : http://plone.org/products/dexterity/documentation/manual/behaviors/testing-behaviors
#    def test_contact_details(self):
#        doc = Document('mydoc')
#        contact_details_adapter = IContactDetails(doc, None)
#        self.assertIsNotNone(contact_details_adapter)
#
#    def test_global_positioning(self):
#        doc = Document('mydoc')
#        global_positioning_adapter = IGlobalPositioning(doc, None)
#        self.assertIsNotNone(global_positioning_adapter)

    def test_contact_details_fields(self):
        item = self.testitem
        self.assertIsNone(item.getAttributes())
        item.phone = '0655443322'
        item.email = 'toto@example.com'
        self.assertEqual(item.phone, '0655443322')
        self.assertEqual(item.email, 'toto@example.com')
        ### TODO: shouldn't work : how do we test validators here ?
        #item.email = 'toto'
        for attr in ('cell_phone', 'im_handle', 'country', 'zip_code',
                     'city', 'street', 'number', 'additional_address_details'):
            self.assertTrue(hasattr(item, attr))

    def test_global_positioning_fields(self):
        item = self.testitem
        item.latitude = 45.2
        item.longitude = -23.8
        self.assertEqual(item.latitude, 45.2)
        self.assertEqual(item.longitude, -23.8)
        ### TODO: shouldn't work : how do we test validators here ?
        #item.longitude = 91.8
        #self.assertEqual(item.longitude, -23.8)

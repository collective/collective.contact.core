# -*- coding: utf8 -*-
from collective.contact.core.behaviors import IBirthday
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.behaviors import IGlobalPositioning
from collective.contact.core.behaviors import InvalidEmailAddress
from collective.contact.core.behaviors import InvalidPhone
from collective.contact.core.behaviors import validate_email
from collective.contact.core.behaviors import validate_phone
from collective.contact.core.testing import INTEGRATION
from collective.contact.core.tests.base import BaseTest
from plone.app.testing.helpers import setRoles
from plone.app.testing.interfaces import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestBehaviors(unittest.TestCase, BaseTest):
    """Tests behaviors"""

    layer = INTEGRATION

    def setUp(self):
        super(TestBehaviors, self).setUp()
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.login(TEST_USER_NAME)
        self.portal.invokeFactory("testtype", "testitem")
        self.testitem = self.portal["testitem"]

    def test_behaviors_installation(self):
        contact_details_behavior = getUtility(IBehavior, name="collective.contact.core.behaviors.IContactDetails")
        global_positioning_behavior = getUtility(IBehavior, name="collective.contact.core.behaviors.IGlobalPositioning")
        birthday_behavior = getUtility(IBehavior, name="collective.contact.core.behaviors.IBirthday")
        self.assertEqual(contact_details_behavior.interface, IContactDetails)
        self.assertEqual(global_positioning_behavior.interface, IGlobalPositioning)
        self.assertEqual(birthday_behavior.interface, IBirthday)
        IFormFieldProvider.providedBy(contact_details_behavior.interface)
        IFormFieldProvider.providedBy(global_positioning_behavior.interface)
        IFormFieldProvider.providedBy(birthday_behavior.interface)

    def test_contact_details_fields(self):
        item = self.testitem
        for attr in (
            "country",
            "region",
            "zip_code",
            "city",
            "street",
            "number",
            "im_handle",
            "cell_phone",
            "phone",
            "email",
            "fax",
            "website",
            "additional_address_details",
            "birthday",
        ):
            self.assertTrue(hasattr(item, attr))
        item.phone = "0655443322"
        item.email = "toto@example.com"
        item.zip_code = "59650"
        self.assertEqual(item.phone, "0655443322")
        self.assertEqual(item.email, "toto@example.com")
        self.assertEqual(item.zip_code, "59650")

        # test clear values when use_parent_address is selected
        item.use_parent_address = True
        notify(ObjectModifiedEvent(item))
        self.assertEqual(item.zip_code, None)
        self.assertEqual(item.phone, "0655443322")

    def test_global_positioning_fields(self):
        item = self.testitem
        item.latitude = 45.2
        item.longitude = -23.8
        self.assertEqual(item.latitude, 45.2)
        self.assertEqual(item.longitude, -23.8)

    def test_validate_email(self):
        self.assertTrue(validate_email("toto@example.com"))
        for value in ("toto", "toto@", "toto@example", "to to@example.com"):
            with self.assertRaises(InvalidEmailAddress):
                validate_email(value)
        # the email field uses the validator
        IContactDetails["email"].validate("toto@example.com")
        with self.assertRaises(InvalidEmailAddress):
            IContactDetails["email"].validate("toto@")

    def test_validate_phone(self):
        for value in ("0655443322", "+32 (0)81 23 45 67", ""):
            self.assertTrue(validate_phone(value))
        for value in ("081/23.45.67", "phone", "32+81"):
            with self.assertRaises(InvalidPhone):
                validate_phone(value)
        # the phone field uses the validator
        IContactDetails["phone"].validate("+32 81 23 45 67")
        with self.assertRaises(InvalidPhone):
            IContactDetails["phone"].validate("081/23.45.67")


class TestAddFormDefaults(unittest.TestCase, BaseTest):
    """Tests the computed defaults of the contact details on add forms"""

    layer = INTEGRATION

    def setUp(self):
        super(TestAddFormDefaults, self).setUp()
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.login(TEST_USER_NAME)
        self.mydirectory = self.portal["mydirectory"]
        self.armeedeterre = self.mydirectory["armeedeterre"]
        self.corpsa = self.armeedeterre["corpsa"]
        self.degaulle = self.mydirectory["degaulle"]

    def add_form_widgets(self, container, portal_type):
        """Returns the widgets of the add form of portal_type in container"""
        self.request["URL"] = "{0}/++add++{1}".format(container.absolute_url(), portal_type)
        form = container.restrictedTraverse("++add++{0}".format(portal_type)).form_instance
        form.update()
        widgets = {}
        for group in form.groups:
            widgets.update(group.widgets)
        return widgets

    def test_default_use_parent_address(self):
        # level-0 organization and person in a directory: own address
        for container, portal_type in ((self.mydirectory, "organization"), (self.mydirectory, "person")):
            widget = self.add_form_widgets(container, portal_type)["IContactDetails.use_parent_address"]
            self.assertEqual(widget.value, [], portal_type)
        # sub organization, position, held position: parent address
        for container, portal_type in (
            (self.corpsa, "organization"),
            (self.armeedeterre, "position"),
            (self.degaulle, "held_position"),
        ):
            widget = self.add_form_widgets(container, portal_type)["IContactDetails.use_parent_address"]
            self.assertEqual(widget.value, ["selected"], portal_type)

    def test_get_parent_address(self):
        # in a directory, there is no parent address
        widget = self.add_form_widgets(self.mydirectory, "organization")["IContactDetails.parent_address"]
        self.assertNotIn("rue", widget.render())
        # in an organization, the parent address is the organization one
        html = self.add_form_widgets(self.corpsa, "organization")["IContactDetails.parent_address"].render()
        self.assertIn("rue Philibert Lucot", html)
        self.assertIn("Orléans", html)
        # in a person, the parent address is the person one
        html = self.add_form_widgets(self.degaulle, "held_position")["IContactDetails.parent_address"].render()
        self.assertIn("rue Jean Moulin", html)

# -*- coding: utf8 -*-
from collective.contact.core.testing import INTEGRATION
from collective.contact.core.tests.base import BaseTest
from collective.contact.widget.interfaces import IContactWidgetSettings
from collective.contact.widget.schema import ContactChoice
from collective.contact.widget.source import ContactSourceBinder
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.interfaces import IFieldWidget
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class TestAddContact(unittest.TestCase, BaseTest):
    """Tests the add contact forms"""

    layer = INTEGRATION

    def setUp(self):
        super(TestAddContact, self).setUp()
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.login(TEST_USER_NAME)
        self.mydirectory = self.portal["mydirectory"]
        self.degaulle = self.mydirectory["degaulle"]
        self.rambo = self.mydirectory["rambo"]
        self.armeedeterre = self.mydirectory["armeedeterre"]
        self.corpsa = self.armeedeterre["corpsa"]
        self.general_adt = self.armeedeterre["general_adt"]

    def submit(self, context, form_name, button="save", **contacts):
        """Submits the form with the given contacts and returns the redirect url"""
        # the request caches the previously submitted values
        for key in [key for key in self.request.other if key.startswith("oform.")]:
            del self.request.other[key]
        self.request.form.clear()
        self.request.response.headers.pop("location", None)
        self.request.response.setStatus(200)
        for name, obj in contacts.items():
            self.request.form["oform.widgets.{0}".format(name)] = "/".join(obj.getPhysicalPath())
        self.request.form["oform.buttons.{0}".format(button)] = "Add"
        form = context.restrictedTraverse(form_name)
        form()
        return self.request.response.getHeader("location")

    def new_held_position(self):
        """Returns the held position added to rambo"""
        new_ids = [oid for oid in self.rambo.objectIds() if oid != "brigadelh"]
        self.assertEqual(len(new_ids), 1)
        return self.rambo[new_ids[0]]

    def messages(self):
        return [message.message for message in IStatusMessage(self.request).show()]

    def test_createAndAdd(self):
        # nothing selected: nothing is done
        self.assertIsNone(self.submit(self.mydirectory, "@@add-contact"))
        # only an organization: redirect to it
        self.assertEqual(
            self.submit(self.mydirectory, "@@add-contact", organization=self.corpsa), self.corpsa.absolute_url()
        )
        # only a person: redirect to it
        self.assertEqual(self.submit(self.mydirectory, "@@add-contact", person=self.rambo), self.rambo.absolute_url())
        self.assertEqual(self.rambo.objectIds(), ["brigadelh"])
        # a person and an organization: a held position is created in the person
        url = self.submit(self.mydirectory, "@@add-contact", person=self.rambo, organization=self.corpsa)
        held_position = self.new_held_position()
        self.assertEqual(held_position.portal_type, "held_position")
        self.assertEqual(held_position.get_organization(), self.corpsa)
        self.assertIsNone(held_position.get_position())
        self.assertEqual(url, held_position.absolute_url() + "/view")
        self.assertIn("Item created", self.messages())
        # a person, an organization and a position: the held position is linked to the position
        api.content.delete(held_position)
        self.submit(
            self.mydirectory,
            "@@add-contact",
            person=self.rambo,
            organization=self.armeedeterre,
            position=self.general_adt,
        )
        held_position = self.new_held_position()
        self.assertEqual(held_position.get_position(), self.general_adt)
        self.assertEqual(held_position.get_organization(), self.armeedeterre)
        self.assertIn(held_position, self.general_adt.get_held_positions())

    def test_handleCancel(self):
        url = self.submit(self.mydirectory, "@@add-contact", button="cancel", person=self.rambo)
        self.assertEqual(url, self.mydirectory.absolute_url())
        self.assertEqual(self.rambo.objectIds(), ["brigadelh"])
        self.assertIn("Add New Item operation cancelled", self.messages())

    def test_add_held_position(self):
        """@@add-held-position requires the organization and the person"""
        self.assertIsNone(self.submit(self.mydirectory, "@@add-held-position", organization=self.corpsa))
        self.assertIsNone(self.submit(self.mydirectory, "@@add-held-position", person=self.rambo))
        self.assertEqual(self.rambo.objectIds(), ["brigadelh"])
        url = self.submit(self.mydirectory, "@@add-held-position", person=self.rambo, organization=self.corpsa)
        self.assertEqual(url, self.new_held_position().absolute_url() + "/view")

    def test_add_contact_from_organization(self):
        form = self.corpsa.restrictedTraverse("@@add-contact")
        form.update()
        self.assertEqual(list(form.widgets["organization"].value), ["/plone/mydirectory/armeedeterre/corpsa"])
        self.assertEqual(list(form.widgets["position"].value), [])
        # the add contact link of an organization opens this form
        html = self.corpsa.restrictedTraverse("view")()
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/corpsa/@@add-contact"', html)

    def test_add_contact_from_position(self):
        form = self.general_adt.restrictedTraverse("@@add-contact")
        form.update()
        self.assertEqual(list(form.widgets["organization"].value), ["/plone/mydirectory/armeedeterre"])
        self.assertEqual(list(form.widgets["position"].value), ["/plone/mydirectory/armeedeterre/general_adt"])
        # the add contact link of a position opens this form
        html = self.general_adt.restrictedTraverse("view")()
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/general_adt/@@add-contact"', html)

    def test_add_organization(self):
        """@@add-organization redirects to the selected position or organization"""
        self.assertEqual(
            self.submit(self.mydirectory, "@@add-organization", organization=self.armeedeterre),
            self.armeedeterre.absolute_url(),
        )
        self.assertEqual(
            self.submit(
                self.mydirectory, "@@add-organization", organization=self.armeedeterre, position=self.general_adt
            ),
            self.general_adt.absolute_url(),
        )

    def test_masterselect_provider(self):
        """The add forms include the script showing the held position fields"""
        html = self.mydirectory.restrictedTraverse("@@add-held-position")()
        self.assertIn("var add_held_position_form = true;", html)
        html = self.mydirectory.restrictedTraverse("@@add-contact")()
        self.assertIn("var add_held_position_form = false;", html)
        self.assertIn('id="oform"', html)

    @unittest.expectedFailure
    def test_add_organization_without_selection(self):
        """Bug kept from Plone 4: submitting @@add-organization without selection raises NotImplementedError
        (handleAdd sets _finishedAdd without redirect and z3c.form AddForm.nextURL is not implemented)"""
        self.assertIsNone(self.submit(self.mydirectory, "@@add-organization"))


class TestContactWidgetSettings(unittest.TestCase, BaseTest):
    """Tests the add links of the contact widgets"""

    layer = INTEGRATION

    def setUp(self):
        super(TestContactWidgetSettings, self).setUp()
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.login(TEST_USER_NAME)
        self.mydirectory = self.portal["mydirectory"]
        self.settings = getUtility(IContactWidgetSettings)

    def add_contact_infos(self, context, **kwargs):
        addlink = kwargs.pop("addlink", True)
        field = ContactChoice(
            __name__="contact", title="Contact", addlink=addlink, source=ContactSourceBinder(**kwargs)
        )
        field = field.bind(context)
        widget = getMultiAdapter((field, self.request), IFieldWidget)
        widget.context = context
        return self.settings.add_contact_infos(widget)

    def test_add_contact_infos(self):
        directory_url = self.mydirectory.absolute_url()
        # one type
        infos = self.add_contact_infos(self.portal, portal_type=("organization",))
        self.assertTrue(infos["close_on_click"])
        self.assertEqual(len(infos["actions"]), 1)
        self.assertEqual(infos["actions"][0]["url"], directory_url + "/++add++organization")
        self.assertEqual(infos["actions"][0]["label"].mapping["name"], "Organization")
        infos = self.add_contact_infos(self.portal, portal_type=("person",))
        self.assertEqual(infos["actions"][0]["url"], directory_url + "/++add++person")
        # held positions: the add held position form
        infos = self.add_contact_infos(self.portal, portal_type=("held_position",))
        self.assertFalse(infos["close_on_click"])
        self.assertEqual(infos["actions"][0]["url"], directory_url + "/@@add-held-position")
        self.assertEqual(infos["actions"][0]["klass"], "addnew")
        # held positions related to a position: the form is prefilled
        infos = self.add_contact_infos(
            self.portal,
            portal_type=("held_position",),
            relations={"position": "/plone/mydirectory/armeedeterre/general_adt"},
        )
        self.assertEqual(
            infos["actions"][0]["url"],
            directory_url + "/@@add-held-position?oform.widgets.position="
            "/plone/mydirectory/armeedeterre/general_adt",
        )
        # organization or position: the add organization form
        infos = self.add_contact_infos(self.portal, portal_type=("organization", "position"))
        self.assertFalse(infos["close_on_click"])
        self.assertEqual(infos["actions"][0]["url"], directory_url + "/@@add-organization")
        # other types: the add contact form
        infos = self.add_contact_infos(self.portal, portal_type=("organization", "person", "held_position"))
        self.assertEqual(infos["actions"][0]["url"], directory_url + "/@@add-contact")
        # no add link
        self.assertEqual(self.add_contact_infos(self.portal, portal_type=("person",), addlink=False)["actions"], [])
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        self.assertEqual(self.add_contact_infos(self.portal, portal_type=("person",))["actions"], [])

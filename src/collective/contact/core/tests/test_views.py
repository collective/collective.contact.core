# -*- coding: utf8 -*-
from collective.contact.core.behaviors import ADDRESS_FIELDS
from collective.contact.core.testing import INTEGRATION
from collective.contact.core.tests.base import BaseTest
from plone import api
from plone.app.testing.helpers import setRoles
from plone.app.testing.interfaces import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from zope.security.management import endInteraction
from zope.security.management import newInteraction

import json
import unittest


TTW_MODEL = """<model xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema>
    <field name="nickname" type="zope.schema.TextLine">
      <title>Nickname</title>
      <required>False</required>
    </field>
  </schema>
</model>"""


class TestView(unittest.TestCase, BaseTest):

    layer = INTEGRATION

    def setUp(self):
        super(TestView, self).setUp()
        self.login(TEST_USER_NAME)
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        mydirectory = self.portal["mydirectory"]
        self.degaulle = mydirectory["degaulle"]
        self.adt = self.degaulle["adt"]
        self.gadt = self.degaulle["gadt"]
        self.pepper = mydirectory["pepper"]
        self.sergent_pepper = self.pepper["sergent_pepper"]
        self.rambo = mydirectory["rambo"]
        self.armeedeterre = mydirectory["armeedeterre"]
        self.corpsa = self.armeedeterre["corpsa"]
        self.divisionalpha = self.corpsa["divisionalpha"]
        self.regimenth = self.divisionalpha["regimenth"]
        self.brigadelh = self.regimenth["brigadelh"]
        self.general_adt = self.armeedeterre["general_adt"]
        self.sergent_lh = self.brigadelh["sergent_lh"]
        self.draper = mydirectory["draper"]
        self.captain_crunch = self.draper["captain_crunch"]
        self.mydirectory = mydirectory

    def render_with_interaction(self, view):
        """Renders a view having contact widgets (z3c.formwidget.query needs an interaction)"""
        newInteraction()
        try:
            view.update()
            return view.render()
        finally:
            endInteraction()


class TestAddressView(TestView):

    def test_degaulle_address_view(self):
        address_view = self.degaulle.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data["country"], "France")
        self.assertEqual(data["number"], "6bis")
        self.assertEqual(data["street"], "rue Jean Moulin")
        self.assertEqual(data["city"], "Colombey les deux églises")
        self.assertEqual(data["zip_code"], "52330")
        self.assertEqual(data["region"], "")
        self.assertEqual(data["additional_address_details"], "bâtiment D")

    def test_pepper_address_view(self):
        address_view = self.pepper.restrictedTraverse("@@address")
        data = address_view.namespace()
        for field in ADDRESS_FIELDS:
            self.assertIn(field, data)
        self.assertEqual(data["country"], "England")
        self.assertEqual(data["city"], "Liverpool")

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
        self.assertEqual(data["number"], "11")
        self.assertEqual(data["street"], "rue de l'harmonie")
        self.assertEqual(data["city"], "Villeneuve d'Ascq")
        self.assertEqual(data["zip_code"], "59650")
        self.assertEqual(data["region"], "")
        self.assertEqual(data["additional_address_details"], "")

    def test_contact_details_render_address(self):
        view = self.corpsa.restrictedTraverse("@@contactdetails")
        view.update()
        html = view.render_address()
        self.assertIn('<div class="street-address">rue Philibert Lucot', html)
        self.assertIn('<span class="locality">Orléans</span>', html)
        self.assertNotIn("tal:", html)
        # no address information
        view = self.rambo.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertNotIn("Address", view.render_address())


class TestContactView(TestView):

    def xtest_contact_view(self):
        view = self.gadt.restrictedTraverse("view")
        view.update()

        self.assertEqual(view.fullname, "Général Charles De Gaulle")
        self.assertEqual([self.armeedeterre], view.organizations)
        self.assertEqual(view.birthday, "Nov 22, 1901")

        # address is acquired from degaulle
        address = view.address
        self.assertEqual(address["number"], "6bis")
        self.assertEqual(address["street"], "rue Jean Moulin")
        self.assertEqual(address["city"], "Colombey les deux églises")
        self.assertEqual(address["zip_code"], "52330")
        self.assertEqual(address["region"], "")
        self.assertEqual(address["additional_address_details"], "bâtiment D")

    def xtest_empty_fields(self):
        view = self.captain_crunch.restrictedTraverse("view")
        view.update()
        self.assertEqual(view.start_date, "")
        self.assertEqual(view.end_date, "")
        self.assertEqual(view.birthday, "")
        self.assertEqual(view.gender, "")
        self.assertEqual(view.photo, "")

    def xtest_contact_details_acquisition(self):
        view = self.sergent_pepper.restrictedTraverse("view")
        view.update()
        self.assertEqual(view.fullname, "Sergent Pepper")
        self.assertEqual(self.sergent_lh, view.position)
        organizations = view.organizations
        self.assertEqual(
            [self.armeedeterre, self.corpsa, self.divisionalpha, self.regimenth, self.brigadelh], organizations
        )

        # Person email comes before Position email
        self.assertEqual(view.contact_details["email"], "sgt.pepper@armees.fr")
        self.assertEqual(view.contact_details["phone"], "0288552211")
        self.assertEqual(view.contact_details["cell_phone"], "0654875233")
        self.assertEqual(view.contact_details["im_handle"], "brigade_lh@jabber.org")

        # Everything in Sgt Pepper's address is acquired from Régiment H
        address = view.contact_details["address"]
        self.assertEqual(address["number"], "11")
        self.assertEqual(address["street"], "rue de l'harmonie")
        self.assertEqual(address["city"], "Villeneuve d'Ascq")
        self.assertEqual(address["zip_code"], "59650")
        self.assertEqual(address["region"], "")
        self.assertEqual(address["additional_address_details"], "")

    def test_held_position_view(self):
        view = self.gadt.restrictedTraverse("view")
        html = self.render_with_interaction(view)
        self.assertEqual(view.fullname, "Général Charles De Gaulle")
        self.assertEqual(view.person, self.degaulle)
        self.assertEqual(view.position, self.general_adt)
        self.assertEqual([self.armeedeterre], view.organizations)
        self.assertIn(view.start_date, ("May 25, 1940", "1940-05-25"))
        self.assertIn(view.end_date, ("Nov 09, 1970", "1970-11-09"))
        self.assertIn(view.birthday, ("Nov 22, 1901", "1901-11-22"))
        self.assertEqual(view.gender, "M")
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre"', html)
        self.assertIn("0987654321", html)
        # empty fields
        view = self.captain_crunch.restrictedTraverse("view")
        self.render_with_interaction(view)
        self.assertEqual(view.start_date, "")
        self.assertEqual(view.end_date, "")
        self.assertEqual(view.birthday, "")
        self.assertEqual(view.gender, "")
        self.assertEqual(view.position, self.divisionalpha["capitaine_alpha"])

    def test_held_position_basefields_view(self):
        view = self.gadt.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(view.title, "Général Charles De Gaulle, Émissaire OTAN (Armée de terre)")
        self.assertEqual(view.position, self.general_adt)
        self.assertIn(view.start_date, ("May 25, 1940", "1940-05-25"))
        html = view()
        self.assertIn("Général Charles De Gaulle, Émissaire OTAN (Armée de terre)", html)
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/general_adt"', html)
        self.assertIn('href="http://nohost/plone/mydirectory/degaulle/gadt/edit"', html)
        # held position without position
        view = self.adt.restrictedTraverse("@@basefields")
        view.update()
        self.assertIsNone(view.position)
        self.assertEqual(view.title, "Général Charles De Gaulle (Armée de terre)")

    def test_nofallbackcontactdetails_view(self):
        # with fallback, details come from the position
        view = self.gadt.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details["email"], "general@armees.fr")
        self.assertEqual(view.contact_details["phone"], "0987654321")
        # without fallback, only the held position details
        view = self.gadt.restrictedTraverse("@@nofallbackcontactdetails")
        view.update()
        self.assertEqual(view.contact_details["email"], "")
        self.assertEqual(view.contact_details["phone"], "0987654321")
        html = view()
        self.assertIn("0987654321", html)
        self.assertNotIn("general@armees.fr", html)


class TestPositionView(TestView):

    def test_position_basefields_view(self):
        view = self.sergent_lh.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(
            view.name,
            "Sergent de la brigade LH (Armée de terre / Corps A / Division Alpha / " "Régiment H / Brigade LH)",
        )
        self.assertEqual(view.type, "Sergeant")

    def test_position_view(self):
        view = self.sergent_lh.restrictedTraverse("view")
        view.update()
        organizations = view.organizations
        self.assertEqual(
            [self.armeedeterre, self.corpsa, self.divisionalpha, self.regimenth, self.brigadelh], organizations
        )

    def test_position_contact_details_view(self):
        view = self.sergent_lh.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details["email"], "brigade_lh@armees.fr")

        address = view.contact_details["address"]
        self.assertEqual(address["number"], "11")
        self.assertEqual(address["street"], "rue de l'harmonie")
        self.assertEqual(address["city"], "Villeneuve d'Ascq")
        self.assertEqual(address["zip_code"], "59650")
        self.assertEqual(address["region"], "")
        self.assertEqual(address["additional_address_details"], "")


class TestOrganizationView(TestView):

    def test_organization_basefields_view(self):
        view = self.corpsa.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(view.name, "Armée de terre / Corps A")
        self.assertEqual(view.type, "Corps")

    def test_organization_view(self):
        view = self.corpsa.restrictedTraverse("view")
        view.update()
        parent_organizations = view.parent_organizations
        self.assertEqual([self.armeedeterre], parent_organizations)

    def test_organization_contact_details_view(self):
        view = self.corpsa.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details["email"], "contact@armees.fr")

        address = view.contact_details["address"]
        self.assertEqual(address["number"], "")
        self.assertEqual(address["street"], "rue Philibert Lucot")
        self.assertEqual(address["city"], "Orléans")
        self.assertEqual(address["zip_code"], "")
        self.assertEqual(address["region"], "")
        self.assertEqual(address["country"], "France")
        self.assertEqual(address["additional_address_details"], "")

    def test_sub_organizations(self):
        view = self.armeedeterre.restrictedTraverse("view")
        view.update()
        sub_organizations_names = [e.Title for e in view.sub_organizations]
        self.assertEqual(set(["Corps A", "Corps B"]), set(sub_organizations_names))
        # no sub-organizations
        view = self.brigadelh.restrictedTraverse("view")
        view.update()
        self.assertEqual(0, len(view.sub_organizations))

    def test_positions(self):
        view = self.armeedeterre.restrictedTraverse("view")
        view.update()
        positions_names = [e.Title() for e in view.positions]
        self.assertEqual(set(["Général de l'armée de terre"]), set(positions_names))
        # no_positions
        view = self.corpsa.restrictedTraverse("view")
        view.update()
        self.assertEqual(0, len(view.positions))

    def test_organization_basefields_render(self):
        self.corpsa.description = "Le corps A de l'armée"
        html = self.corpsa.restrictedTraverse("@@basefields")()
        self.assertIn("Armée de terre / Corps A", html)
        self.assertIn("Corps", html)
        self.assertIn("Le corps A de l'armée", html)
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/corpsa/edit"', html)

    def test_suborganizations_view(self):
        html = self.armeedeterre.restrictedTraverse("@@suborganizations")()
        self.assertIn('id="sub_organizations"', html)
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/corpsa"', html)
        self.assertIn("Corps A", html)
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/corpsb"', html)
        self.assertLess(html.index("Corps A"), html.index("Corps B"))
        # no sub-organizations
        html = self.brigadelh.restrictedTraverse("@@suborganizations")()
        self.assertNotIn('id="sub_organizations"', html)

    def test_othercontacts(self):
        view = self.armeedeterre.restrictedTraverse("@@othercontacts")
        view()
        contact = view.othercontacts[0]
        self.assertEqual(contact["title"], "Général Charles De Gaulle")
        self.assertEqual(contact["held_position"], "(Armée de terre)")
        self.assertIsNone(contact["label"])
        self.assertEqual(contact["obj"], self.adt)
        self.assertEqual(contact["email"], None)
        self.assertIsNone(contact["phone"])
        self.assertIsNone(contact["cell_phone"])
        self.assertIsNone(contact["fax"])
        self.assertIsNone(contact["im_handle"])
        self.assertEqual(contact["website"], None)


class TestPersonView(TestView):

    def test_person_basefields_view(self):
        view = self.degaulle.restrictedTraverse("@@basefields")
        view.update()
        self.assertEqual(view.name, "Général Charles De Gaulle")
        self.assertEqual(view.gender, "M")
        self.assertIn(view.birthday, ("Nov 22, 1901", "1901-11-22"))

    def test_person_view(self):
        view = self.degaulle.restrictedTraverse("view")
        view.update()
        self.assertTrue(view.show_contact_details)
        html = view.render()
        self.assertIn("Général Charles De Gaulle", html)
        self.assertIn("charles.de.gaulle@private.com", html)
        self.assertIn('id="held_positions"', html)
        self.assertIn('href="http://nohost/plone/mydirectory/degaulle/gadt/view"', html)

    def test_person_contact_details_view(self):
        view = self.degaulle.restrictedTraverse("@@contactdetails")
        view.update()
        self.assertEqual(view.contact_details["email"], "charles.de.gaulle@private.com")
        self.assertEqual(view.contact_details["phone"], "")
        self.assertEqual(view.contact_details["cell_phone"], "")
        self.assertEqual(view.contact_details["im_handle"], "")

        address = view.contact_details["address"]
        self.assertEqual(address["number"], "6bis")
        self.assertEqual(address["street"], "rue Jean Moulin")
        self.assertEqual(address["city"], "Colombey les deux églises")
        self.assertEqual(address["zip_code"], "52330")
        self.assertEqual(address["region"], "")
        self.assertEqual(address["country"], "France")
        self.assertEqual(address["additional_address_details"], "bâtiment D")

    def test_person_held_positions_view(self):
        view = self.degaulle.restrictedTraverse("@@heldpositions")
        view()
        held_positions = view.held_positions
        self.assertEqual(len(held_positions), 2)
        first = held_positions[0]
        self.assertEqual(self.adt, first["object"])
        self.assertEqual(self.adt.Title(), first["title"])
        self.assertIn(first["start_date"], ["May 25, 1940", "1940-05-25"])
        self.assertEqual(self.armeedeterre, first["organization"])

        second = held_positions[1]
        self.assertEqual(self.gadt, second["object"])
        self.assertEqual(self.gadt.Title(), second["title"])
        self.assertIn(second["start_date"], ["May 25, 1940", "1940-05-25"])
        self.assertIn(second["end_date"], ["Nov 09, 1970", "1970-11-09"])
        self.assertEqual(self.armeedeterre, second["organization"])

    def test_person_held_positions_render(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        html = self.degaulle.restrictedTraverse("@@heldpositions")()
        for url in ("http://nohost/plone/mydirectory/degaulle/adt", "http://nohost/plone/mydirectory/degaulle/gadt"):
            self.assertIn('href="{0}/view"'.format(url), html)
            self.assertIn('href="{0}/edit"'.format(url), html)
            self.assertIn('href="{0}/delete_confirmation"'.format(url), html)
        self.assertIn("Émissaire OTAN (Armée de terre)", html)
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre"', html)
        # held position and organization icons (Plone 6: icons of plone.icon.contenttype/* registry records)
        self.assertIn("person-badge.svg", html)
        self.assertIn("bi-diagram-3-fill", html)
        self.assertNotIn("file-earmark-person-fill", html)
        # no edit nor delete links without permission
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        view = self.degaulle.restrictedTraverse("@@heldpositions")
        html = view()
        self.assertFalse(view.held_positions[0]["can_edit"])
        self.assertFalse(view.held_positions[0]["can_delete"])
        self.assertIn('href="http://nohost/plone/mydirectory/degaulle/gadt/view"', html)
        self.assertNotIn('href="http://nohost/plone/mydirectory/degaulle/gadt/edit"', html)
        self.assertNotIn("delete_confirmation", html)
        # no dates
        html = self.draper.restrictedTraverse("@@heldpositions")()
        self.assertIn("Capitaine de la division Alpha", html)
        self.assertNotIn("Start date", html)
        self.assertNotIn("End date", html)


class TestDirectoryView(TestView):

    def test_directory_view(self):
        view = self.mydirectory.restrictedTraverse("view")
        view.update()
        self.assertEqual(sorted([brain.getId for brain in view.persons]), ["degaulle", "draper", "pepper", "rambo"])
        self.assertEqual([brain.getId for brain in view.organizations], ["armeedeterre"])
        html = view.render()
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre"', html)
        self.assertIn('href="http://nohost/plone/mydirectory/degaulle"', html)


class TestContactVCF(TestView):

    def test_contact_vcf(self):
        vcf = self.gadt.restrictedTraverse("@@contact.vcf")()
        response = self.layer["request"].response
        self.assertEqual(response.getHeader("Content-Type"), "text/x-vCard; charset=utf-8")
        self.assertEqual(response.getHeader("Content-Disposition"), "attachment; filename=gadt.vcf")
        self.assertTrue(vcf.startswith("BEGIN:VCARD"))
        self.assertIn("FN:Charles De Gaulle", vcf)
        self.assertIn("END:VCARD", vcf)


class TestGenderPersonTitleMapping(TestView):

    def test_gender_person_title_mapping(self):
        result = self.portal.restrictedTraverse("@@gender_person_title_mapping.json")()
        self.assertEqual(self.layer["request"].response.getHeader("Content-Type"), "application/json")
        self.assertEqual(json.loads(result), {"M": "Mr", "F": "Mrs"})


class TestTTWFields(TestView):

    def test_ttwfields(self):
        # no field added through the web
        view = self.degaulle.restrictedTraverse("@@ttwfields")
        html = view()
        self.assertEqual(view.ttw_fields, [])
        self.assertNotIn("<label>", html)
        # a field added through the web on person type
        fti = api.portal.get_tool("portal_types")["person"]
        self.addCleanup(fti.manage_changeProperties, model_source=fti.model_source)
        fti.manage_changeProperties(model_source=TTW_MODEL)
        self.degaulle.nickname = "Le grand Charles"
        view = self.degaulle.restrictedTraverse("@@ttwfields")
        html = view()
        self.assertEqual(view.ttw_fields, ["nickname"])
        self.assertIn("Nickname", html)
        self.assertIn("Le grand Charles", html)

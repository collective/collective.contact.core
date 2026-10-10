# -*- coding: utf8 -*-

from collective.contact.core.content.directory import is_valid_identifier
from collective.contact.core.content.organization import InvalidEnterpriseNumber
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.organization import validateEnterpriseNumber
from collective.contact.core.interfaces import IContactCoreParameters
from collective.contact.core.testing import INTEGRATION
from collective.contact.core.tests.base import BaseTest
from collective.contact.widget.schema import ContactChoice
from collective.contact.widget.source import ContactSourceBinder
from plone import api
from plone.app.testing.helpers import setRoles
from plone.app.testing.interfaces import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.dexterity.fti import DexterityFTI
from plone.supermodel import model
from z3c.relationfield.relation import RelationValue
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import datetime
import unittest


class IPositionHolder(model.Schema):
    """Schema of a content that is not a held position but has a `position` relation"""

    position = ContactChoice(
        title="Position",
        required=False,
        source=ContactSourceBinder(portal_type=("organization", "position")),
    )


class TestContentTypes(unittest.TestCase, BaseTest):
    """Base class to test new content types"""

    layer = INTEGRATION

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.portal = self.layer["portal"]
        self.mydirectory = self.portal["mydirectory"]
        self.degaulle = self.mydirectory["degaulle"]
        self.pepper = self.mydirectory["pepper"]
        self.armeedeterre = self.mydirectory["armeedeterre"]
        self.corpsa = self.armeedeterre["corpsa"]
        self.corpsb = self.armeedeterre["corpsb"]
        self.divisionalpha = self.corpsa["divisionalpha"]
        self.regimenth = self.divisionalpha["regimenth"]
        self.brigadelh = self.regimenth["brigadelh"]
        self.general_adt = self.armeedeterre["general_adt"]
        self.sergent_lh = self.brigadelh["sergent_lh"]
        self.adt = self.degaulle["adt"]
        self.gadt = self.degaulle["gadt"]
        self.sergent_pepper = self.pepper["sergent_pepper"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.login(TEST_USER_NAME)

    def add_position_holder(self, target):
        """Adds a non held position content whose `position` field points to target"""
        if "position_holder" not in self.portal.portal_types:
            fti = DexterityFTI(
                "position_holder",
                klass="plone.dexterity.content.Item",
                global_allow=True,
                schema="collective.contact.core.tests.test_content_types.IPositionHolder",
            )
            self.portal.portal_types._setObject("position_holder", fti)
        intids = getUtility(IIntIds)
        holder = api.content.create(
            container=self.portal, type="position_holder", id="holder", position=RelationValue(intids.getId(target))
        )
        # the relation is cataloged like the held position ones
        relations = getUtility(ICatalog).findRelations({"to_id": intids.getId(target), "from_attribute": "position"})
        self.assertIn(holder, [rel.from_object for rel in relations])
        return holder


class TestDirectory(TestContentTypes):

    def test_directory(self):
        self.assertIn("mydirectory", self.portal)
        mydirectory = self.portal["mydirectory"]
        self.assertEqual("Military directory", mydirectory.Title())
        self.assertIn({"name": "Colonel", "token": "colonel"}, mydirectory.position_types)
        self.assertIn({"name": "Air force", "token": "air_force"}, mydirectory.organization_types)
        self.assertIn({"name": "Regiment", "token": "regiment"}, mydirectory.organization_levels)

    def test_is_valid_identifier(self):
        self.assertFalse(is_valid_identifier("Toto"))
        self.assertTrue(is_valid_identifier("toto"))
        self.assertTrue(is_valid_identifier("toto56"))
        self.assertFalse(is_valid_identifier("toto 56"))
        self.assertTrue(is_valid_identifier("toto-56"))
        self.assertFalse(is_valid_identifier("toto-56@"))
        self.assertFalse(is_valid_identifier("toto-56à"))
        self.assertFalse(is_valid_identifier("toto-56É"))


class TestPerson(TestContentTypes):

    def test_person(self):
        self.assertIn("degaulle", self.mydirectory)
        degaulle = self.degaulle
        self.assertEqual("Général Charles De Gaulle", degaulle.Title())
        self.assertEqual("Général Charles De Gaulle", degaulle.title)
        self.assertEqual("De Gaulle", degaulle.lastname)
        self.assertEqual("Charles", degaulle.firstname)
        self.assertEqual(datetime.date(1901, 11, 22), degaulle.birthday)

    def test_no_firstname(self):
        pepper = self.mydirectory["pepper"]
        self.assertEqual("Mister Pepper", pepper.Title())

    def test_no_person_title(self):
        rambo = self.mydirectory["rambo"]
        self.assertEqual("John Rambo", rambo.Title())
        # we can't create persons in portal
        with self.assertRaises(ValueError):
            self.portal.invokeFactory("person", "error", {"lastname": "Casper"})

    def test_copy_paste(self):
        cb = self.mydirectory.manage_copyObjects(["pepper"])
        self.mydirectory.manage_pasteObjects(cb)
        self.assertIn("copy_of_pepper", list(self.mydirectory.keys()))


class TestOrganization(TestContentTypes):

    def test_organization(self):
        armeedeterre = self.armeedeterre
        self.assertIn("armeedeterre", self.mydirectory)
        self.assertEqual(armeedeterre.Title(), "Armée de terre")
        self.assertEqual(armeedeterre.enterprise_number, "BE123456789")
        self.assertIn("corpsa", armeedeterre)
        self.assertIn("corpsb", armeedeterre)
        self.assertIn("divisionalpha", self.corpsa)
        self.assertIn("divisionbeta", self.corpsa)
        self.assertIn("regimenth", self.divisionalpha)
        self.assertIn("brigadelh", self.regimenth)
        self.assertIn("armeedeterre", self.divisionalpha.getPhysicalPath())
        self.assertIn("armeedeterre", self.brigadelh.getPhysicalPath())

    def test_get_organizations_chain(self):
        armeedeterre = self.armeedeterre
        corpsa = self.corpsa
        divisionalpha = self.divisionalpha
        self.assertEqual([armeedeterre], self.armeedeterre.get_organizations_chain())
        self.assertEqual([armeedeterre, corpsa, divisionalpha], self.divisionalpha.get_organizations_chain())
        self.assertEqual([corpsa, divisionalpha], self.divisionalpha.get_organizations_chain(first_index=1))
        self.assertEqual([], self.divisionalpha.get_organizations_chain(first_index=50))

    def test_get_root_organization(self):
        armeedeterre = self.armeedeterre
        organizations = [armeedeterre, self.corpsa, self.corpsb, self.divisionalpha, self.regimenth, self.brigadelh]
        for org in organizations:
            self.assertEqual(armeedeterre, org.get_root_organization())

    def test_get_organizations_titles(self):
        corpsa_titles = self.corpsa.get_organizations_titles()
        self.assertIn("Armée de terre", corpsa_titles)
        self.assertIn("Corps A", corpsa_titles)
        self.assertEqual(len(corpsa_titles), 2)

        division_alpha_titles = self.divisionalpha.get_organizations_titles()
        self.assertIn("Armée de terre", division_alpha_titles)
        self.assertIn("Corps A", division_alpha_titles)
        self.assertIn("Division Alpha", division_alpha_titles)
        self.assertEqual(len(division_alpha_titles), 3)

        brigadelh_titles = self.brigadelh.get_organizations_titles()
        self.assertIn("Armée de terre", brigadelh_titles)
        self.assertIn("Corps A", brigadelh_titles)
        self.assertIn("Division Alpha", brigadelh_titles)
        self.assertIn("Régiment H", brigadelh_titles)
        self.assertIn("Brigade LH", brigadelh_titles)
        self.assertEqual(len(brigadelh_titles), 5)

        brigadelh_titles = self.brigadelh.get_organizations_titles(first_index=2)
        self.assertIn("Division Alpha", brigadelh_titles)
        self.assertIn("Régiment H", brigadelh_titles)
        self.assertIn("Brigade LH", brigadelh_titles)
        self.assertEqual(len(brigadelh_titles), 3)

    def test_get_full_title(self):
        self.assertEqual(self.armeedeterre.get_full_title(), "Armée de terre")
        self.assertEqual(
            self.brigadelh.get_full_title(), "Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH"
        )
        self.assertEqual(
            self.brigadelh.get_full_title(separator=" - "),
            "Armée de terre - Corps A - Division Alpha - Régiment H - Brigade LH",
        )
        self.assertEqual(
            self.brigadelh.get_full_title(separator=" - ", first_index=2), "Division Alpha - Régiment H - Brigade LH"
        )

    def test_reindex_suborganization(self):
        before = self.portal.portal_catalog(UID=self.brigadelh.UID())[0].get_full_title
        self.assertEqual(before, "Arm\xe9e de terre / Corps A / Division Alpha / R\xe9giment H / Brigade LH")
        self.armeedeterre.title = "Armée de l'air"
        from zope.lifecycleevent import modified

        modified(self.armeedeterre)
        after = self.portal.portal_catalog(UID=self.brigadelh.UID())[0].get_full_title
        self.assertEqual(after, "Arm\xe9e de l'air / Corps A / Division Alpha / R\xe9giment H / Brigade LH")

    def test_copy_paste(self):
        cb = self.mydirectory.manage_copyObjects(["armeedeterre"])
        self.mydirectory.manage_pasteObjects(cb)
        self.assertIn("copy_of_armeedeterre", list(self.mydirectory.keys()))

    def test_get_positions(self):
        # add some positions to self.armeedeterre
        self.armeedeterre.invokeFactory("position", "colonel_adt", title="Colonel de l'armée de terre")
        self.armeedeterre.invokeFactory("position", "lieutenant_adt", title="Lieutenant de l'armée de terre")
        self.armeedeterre.invokeFactory("position", "sergent_adt", title="Sergent de l'armée de terre")
        self.assertEqual(
            [pos.id for pos in self.armeedeterre.get_positions()],
            ["general_adt", "colonel_adt", "lieutenant_adt", "sergent_adt"],
        )
        # get_positions sorts positions using getObjPositionInParent
        # move 'general_adt' to last position
        self.armeedeterre.moveObjectToPosition("general_adt", len(self.armeedeterre.objectIds()))
        self.assertEqual(
            [pos.id for pos in self.armeedeterre.get_positions()],
            ["colonel_adt", "lieutenant_adt", "sergent_adt", "general_adt"],
        )

    def test_get_held_positions(self):
        # held positions directly linked to the organization (without position)
        self.assertEqual(self.armeedeterre.get_held_positions(), [self.adt])
        self.assertEqual(self.brigadelh.get_held_positions(), [self.mydirectory["rambo"]["brigadelh"]])
        # a held position linked to a position of the organization is not returned
        self.assertEqual(self.corpsa.get_held_positions(), [])
        # only held positions are returned, not other contents having a `position` relation
        self.add_position_holder(self.armeedeterre)
        self.assertEqual(self.armeedeterre.get_held_positions(), [self.adt])

    def test_validateEnterpriseNumber(self):
        self.assertTrue(validateEnterpriseNumber("BE123456789"))
        with self.assertRaises(InvalidEnterpriseNumber):
            validateEnterpriseNumber("BE 123.456.789")
        # the organization field uses the validator
        field = IOrganization["enterprise_number"]
        field.validate("BE123456789")
        with self.assertRaises(InvalidEnterpriseNumber):
            field.validate("BE-123")


class TestPosition(TestContentTypes):

    def test_position(self):
        self.assertIn("general_adt", self.armeedeterre)
        general_adt = self.general_adt
        self.assertEqual(general_adt.Title(), "Général de l'armée de terre")
        self.assertEqual(general_adt.position_type, "general")

    def test_get_full_title(self):
        self.assertEqual(self.general_adt.get_full_title(), "Général de l'armée de terre (Armée de terre)")
        self.assertEqual(
            self.sergent_lh.get_full_title(),
            "Sergent de la brigade LH (Armée de terre / Corps A / Division Alpha / Régiment H / " "Brigade LH)",
        )

    def test_copy_paste(self):
        cb = self.armeedeterre.manage_copyObjects(["general_adt"])
        self.armeedeterre.manage_pasteObjects(cb)
        self.assertIn("copy_of_general_adt", list(self.armeedeterre.keys()))

    def test_get_held_positions(self):
        self.assertEqual(self.general_adt.get_held_positions(), [self.gadt])
        self.assertEqual(self.sergent_lh.get_held_positions(), [self.sergent_pepper])
        # only held positions are returned, not other contents having a `position` relation
        self.add_position_holder(self.general_adt)
        self.assertEqual(self.general_adt.get_held_positions(), [self.gadt])


class TestHeldPosition(TestContentTypes):

    def test_held_position(self):
        degaulle = self.degaulle
        adt = self.adt
        gadt = self.gadt
        pepper = self.pepper
        sergent_pepper = self.sergent_pepper
        self.assertIn("adt", degaulle)
        self.assertEqual(adt.Title(), "(Armée de terre)")
        self.assertEqual(adt.title, "(Armée de terre)")
        self.assertIn("gadt", degaulle)
        self.assertEqual(gadt.Title(), "Émissaire OTAN (Armée de terre)")
        self.assertIn("sergent_pepper", pepper)
        self.assertEqual(
            sergent_pepper.Title(),
            "Sergent de la brigade LH (Armée de terre / Corps A / Division Alpha / Régiment H / " "Brigade LH)",
        )
        self.assertIsNone(sergent_pepper.end_date)

    def test_get_full_title(self):
        self.assertEqual(self.adt.get_full_title(), "Général Charles De Gaulle (Armée de terre)")
        self.assertEqual(self.gadt.get_full_title(), "Général Charles De Gaulle, Émissaire OTAN (Armée de terre)")
        self.assertEqual(
            self.sergent_pepper.get_full_title(),
            "Mister Pepper, Sergent de la brigade LH (Armée de terre / Corps A / Division Alpha / "
            "Régiment H / Brigade LH)",
        )

    def test_get_person_title(self):
        self.assertEqual(self.gadt.get_person_title(), "Général Charles De Gaulle")
        self.assertEqual(self.gadt.get_person_title(include_person_title=False), "Charles De Gaulle")
        api.portal.set_registry_record(name="person_title_in_title", value=False, interface=IContactCoreParameters)
        self.assertEqual(self.gadt.get_person_title(include_person_title=True), "Charles De Gaulle")

    def test_get_person(self):
        pass

    def test_get_position(self):
        pass

    def test_get_organization(self):
        pass

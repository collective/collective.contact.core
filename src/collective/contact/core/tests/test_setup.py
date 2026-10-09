# -*- coding: utf8 -*-
from collective.contact.core.behaviors import IBirthday
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.testing import INTEGRATION
from plone import api
from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.base.utils import get_installer
from plone.behavior.interfaces import IBehavior
from Products.CMFPlone.utils import typesToList
from zope.component import getUtility

import unittest


CONTACT_TYPES = ("organization", "person", "position", "held_position")


class TestSetup(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_is_installed(self):
        """Test if collective.contact.core is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.contact.core"))

    def test_types(self):
        expected = {
            # portal_type: (class, global_allow, allowed_content_types, behaviors)
            "directory": ("directory.Directory", True, ["organization", "person"], [IBasic, INameFromTitle]),
            "organization": (
                "organization.Organization",
                False,
                ["organization", "position"],
                [IBasic, INameFromTitle, IContactDetails],
            ),
            "position": ("position.Position", False, [], [IBasic, INameFromTitle, IContactDetails]),
            "person": ("person.Person", False, ["held_position"], [INameFromTitle, IContactDetails, IBirthday]),
            "held_position": ("held_position.HeldPosition", False, [], [INameFromTitle, IContactDetails]),
        }
        portal_types = api.portal.get_tool("portal_types")
        for portal_type, (klass, global_allow, allowed_types, behaviors) in expected.items():
            fti = portal_types[portal_type]
            self.assertEqual(fti.klass, "collective.contact.core.content.{0}".format(klass))
            self.assertEqual(fti.global_allow, global_allow, portal_type)
            self.assertTrue(fti.filter_content_types, portal_type)
            self.assertEqual(sorted(fti.allowed_content_types), allowed_types, portal_type)
            self.assertEqual(fti.schema_policy, "schema_policy_{0}".format(portal_type))
            interfaces = [getUtility(IBehavior, name=name).interface for name in fti.behaviors]
            for behavior in behaviors:
                self.assertIn(behavior, interfaces, portal_type)
        # a directory can be added anywhere, contacts only in a directory
        self.assertIn("directory", [fti.getId() for fti in self.portal.allowedContentTypes()])
        self.assertEqual(
            sorted([fti.getId() for fti in self.portal["mydirectory"].allowedContentTypes()]),
            ["organization", "person"],
        )

    def test_workflows(self):
        wtool = api.portal.get_tool("portal_workflow")
        for portal_type in CONTACT_TYPES:
            self.assertEqual(wtool.getChainForPortalType(portal_type), ("collective_contact_core_workflow",))
        self.assertNotIn("collective_contact_core_workflow", wtool.getChainForPortalType("directory"))
        workflow = wtool["collective_contact_core_workflow"]
        self.assertEqual(workflow.initial_state, "active")
        self.assertEqual(sorted(workflow.states.objectIds()), ["active", "deactivated"])
        self.assertEqual(api.content.get_state(self.portal["mydirectory"]["degaulle"]["gadt"]), "active")

    def test_catalog(self):
        catalog = api.portal.get_tool("portal_catalog")
        self.assertEqual(catalog.Indexes["email"].meta_type, "FieldIndex")
        for column in ("get_full_title", "sortable_title", "contact_source", "email"):
            self.assertIn(column, catalog.schema())
        brains = catalog(email="contact@armees.fr")
        self.assertEqual([brain.getPath() for brain in brains], ["/plone/mydirectory/armeedeterre"])
        self.assertEqual(brains[0].get_full_title, "Armée de terre")

    def test_navigation(self):
        listed_types = typesToList(self.portal)
        self.assertIn("directory", listed_types)
        for portal_type in CONTACT_TYPES:
            self.assertNotIn(portal_type, listed_types)

    def test_rolemap(self):
        roles = [
            role["name"]
            for role in self.portal.rolesOfPermission("collective.contact.core: Use parent address")
            if role["selected"]
        ]
        self.assertEqual(sorted(roles), ["Manager", "Member"])

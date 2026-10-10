# -*- coding: utf8 -*-

from collective.contact.core.testing import INTEGRATION
from collective.contact.core.tests.base import BaseWorkflowTest
from collective.contact.core.tests.base import create_members

import unittest


USERDEFS = [
    {
        "user": "manager",
        "roles": (
            "Manager",
            "Member",
        ),
        "groups": (),
    },
    {
        "user": "contributor",
        "roles": (
            "Contributor",
            "Member",
        ),
        "groups": (),
    },
    {"user": "member", "roles": ("Member",), "groups": ()},
]


PERSON_PERMISSIONS = {
    "active": {
        "Access contents information": ("manager", "contributor", "member"),
        "Modify portal content": ("manager", "contributor"),
        "View": ("manager", "contributor", "member"),
    },
    "deactivated": {
        "Access contents information": ("manager", "contributor"),
        "Modify portal content": ("manager", "contributor"),
        "View": ("manager", "contributor"),
    },
}


WORKFLOW_TRACK = [
    ("", "active"),
    ("deactivate", "deactivated"),
    ("activate", "active"),
]


class TestSecurity(unittest.TestCase, BaseWorkflowTest):
    """Tests collective.contact.core workflows"""

    layer = INTEGRATION

    def setUp(self):
        super(TestSecurity, self).setUp()
        self.portal = self.layer["portal"]
        create_members(self.portal, USERDEFS)
        self.mydirectory = self.portal["mydirectory"]
        self.degaulle = self.mydirectory["degaulle"]

    def test_person_permissions(self):
        degaulle = self.degaulle
        workflow = self.portal.portal_workflow
        self.login("manager")
        self.assertCheckPermissions(degaulle, PERSON_PERMISSIONS["active"], USERDEFS)

        for transition, state in WORKFLOW_TRACK:
            if transition:
                workflow.doActionFor(degaulle, transition)
            if state:
                self.assertHasState(degaulle, state)
                self.assertCheckPermissions(degaulle, PERSON_PERMISSIONS[state], USERDEFS, stateid=state)

    def test_contact_permissions(self):
        """organization, position and held_position have the same workflow as person"""
        workflow = self.portal.portal_workflow
        armeedeterre = self.mydirectory["armeedeterre"]
        self.login("manager")
        for obj in (armeedeterre, armeedeterre["general_adt"], self.degaulle["gadt"]):
            for transition, state in WORKFLOW_TRACK:
                if transition:
                    workflow.doActionFor(obj, transition)
                self.assertHasState(obj, state)
                self.assertCheckPermissions(obj, PERSON_PERMISSIONS[state], USERDEFS, stateid=state)

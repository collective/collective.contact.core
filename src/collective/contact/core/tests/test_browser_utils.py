# -*- coding: utf8 -*-
from collective.contact.core.browser.utils import get_object_from_referer
from collective.contact.core.browser.utils import get_object_from_request
from collective.contact.core.browser.utils import get_valid_url
from collective.contact.core.testing import FUNCTIONAL
from collective.contact.core.testing import logged_actions
from collective.contact.core.tests.base import BaseTest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from zope.security.management import endInteraction
from zope.security.management import newInteraction

import unittest


def rmv_uid(idx):
    return logged_actions[idx][logged_actions[idx].index(" PATH=") + 1 :]


class TestBrowserUtils(unittest.TestCase, BaseTest):

    layer = FUNCTIONAL

    def setUp(self):
        super(TestBrowserUtils, self).setUp()
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

    def call_view(self, obj, view_name):
        if len(obj.REQUEST["PARENTS"]) == 1:
            obj.REQUEST["PARENTS"].insert(0, obj)
        else:
            obj.REQUEST["PARENTS"][0] = obj
        obj.REQUEST["URL"] = "{}/{}".format(obj.absolute_url(), view_name)
        view = obj.restrictedTraverse(view_name)
        view.update()
        view.render()

    def test_audit_access(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.call_view(self.armeedeterre, "view")
        self.assertEqual(len(logged_actions), 0)
        # we set the registry record to True
        api.portal.set_registry_record(
            "collective.contact.core.interfaces.IContactCoreParameters." "audit_contact_access", True
        )
        api.portal.set_registry_record(
            "collective.contact.core.interfaces.IContactCoreParameters.audit_contact_types", []
        )
        # # VIEW
        # check organisation view
        self.call_view(self.armeedeterre, "view")
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(
            rmv_uid(0), "PATH=/mydirectory/armeedeterre " "CTX_PATH=/mydirectory/armeedeterre CASE=contact_view"
        )
        self.assertEqual(
            rmv_uid(1), "PATH=/mydirectory/degaulle/adt " "CTX_PATH=/mydirectory/armeedeterre CASE=contact_view"
        )
        # check sub organization view
        logged_actions[:] = []  # clear
        self.call_view(self.brigadelh, "view")
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(
            rmv_uid(0),
            "PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh "
            "CTX_PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh"
            " CASE=contact_view",
        )
        self.assertEqual(
            rmv_uid(1),
            "PATH=/mydirectory/rambo/brigadelh "
            "CTX_PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh"
            " CASE=contact_view",
        )
        # check person view
        logged_actions[:] = []  # clear
        self.call_view(self.degaulle, "view")
        self.assertEqual(len(logged_actions), 5)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle " "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        self.assertEqual(
            rmv_uid(1), "PATH=/mydirectory/degaulle/adt " "CTX_PATH=/mydirectory/degaulle CASE=contact_view"
        )
        self.assertEqual(
            rmv_uid(2), "PATH=/mydirectory/armeedeterre " "CTX_PATH=/mydirectory/degaulle CASE=contact_view"
        )
        self.assertEqual(
            rmv_uid(3), "PATH=/mydirectory/degaulle/gadt " "CTX_PATH=/mydirectory/degaulle CASE=contact_view"
        )
        self.assertEqual(
            rmv_uid(4), "PATH=/mydirectory/armeedeterre " "CTX_PATH=/mydirectory/degaulle CASE=contact_view"
        )
        # check position view
        logged_actions[:] = []  # clear
        self.call_view(self.general_adt, "view")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(
            rmv_uid(0),
            "PATH=/mydirectory/armeedeterre/general_adt "
            "CTX_PATH=/mydirectory/armeedeterre/general_adt CASE=contact_view",
        )
        # check held_position view
        logged_actions[:] = []  # clear
        # necessary for z3c.formwidget.query widget initialization... to avoid NoInteraction error
        newInteraction()
        self.call_view(self.gadt, "view")
        endInteraction()
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(
            rmv_uid(0),
            "PATH=/mydirectory/armeedeterre/general_adt " "CTX_PATH=/mydirectory/degaulle/gadt CASE=contact_view",
        )
        self.assertEqual(
            rmv_uid(1), "PATH=/mydirectory/degaulle/gadt " "CTX_PATH=/mydirectory/degaulle/gadt CASE=contact_view"
        )
        # # EDIT
        # check organisation edit
        logged_actions[:] = []  # clear
        self.call_view(self.armeedeterre, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(
            rmv_uid(0), "PATH=/mydirectory/armeedeterre " "CTX_PATH=/mydirectory/armeedeterre CASE=contact_edit"
        )
        # check sub organization edit
        logged_actions[:] = []  # clear
        self.call_view(self.brigadelh, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(
            rmv_uid(0),
            "PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh "
            "CTX_PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh"
            " CASE=contact_edit",
        )
        # check person edit
        logged_actions[:] = []  # clear
        self.call_view(self.degaulle, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle " "CTX_PATH=/mydirectory/degaulle CASE=contact_edit")
        # check position edit
        logged_actions[:] = []  # clear
        self.call_view(self.general_adt, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(
            rmv_uid(0),
            "PATH=/mydirectory/armeedeterre/general_adt "
            "CTX_PATH=/mydirectory/armeedeterre/general_adt CASE=contact_edit",
        )
        # check held_position edit
        logged_actions[:] = []  # clear
        # necessary for z3c.formwidget.query widget initialization... to avoid NoInteraction error
        newInteraction()
        self.call_view(self.gadt, "@@edit")
        endInteraction()
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(
            rmv_uid(0), "PATH=/mydirectory/degaulle/gadt " "CTX_PATH=/mydirectory/degaulle/gadt CASE=contact_edit"
        )
        # # OVERLAY
        # check directory overlay
        logged_actions[:] = []
        self.call_view(self.mydirectory, "view")
        self.assertEqual(len(logged_actions), 0)
        # simulate overlay
        self.armeedeterre.REQUEST["HTTP_REFERER"] = "http://nohost/plone/mydirectory"
        self.armeedeterre.REQUEST["ajax_load"] = "12345678"
        self.call_view(self.armeedeterre, "view")
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre " "CTX_PATH=/mydirectory CASE=contact_overlay")
        self.assertEqual(rmv_uid(1), "PATH=/mydirectory/degaulle/adt " "CTX_PATH=/mydirectory CASE=contact_overlay")
        # # # we filter on person only
        api.portal.set_registry_record(
            "collective.contact.core.interfaces.IContactCoreParameters.audit_contact_types", ["person"]
        )
        del self.armeedeterre.REQUEST.other["ajax_load"]
        # # VIEW
        # check organisation view
        logged_actions[:] = []  # clear
        self.call_view(self.armeedeterre, "view")
        self.assertEqual(len(logged_actions), 0)
        # check sub organization view
        logged_actions[:] = []  # clear
        self.call_view(self.brigadelh, "view")
        self.assertEqual(len(logged_actions), 0)
        # check person view
        logged_actions[:] = []  # clear
        self.call_view(self.degaulle, "view")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle " "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        # check position view
        logged_actions[:] = []  # clear
        self.call_view(self.general_adt, "view")
        self.assertEqual(len(logged_actions), 0)
        # check held_position view
        logged_actions[:] = []  # clear
        # necessary for z3c.formwidget.query widget initialization... to avoid NoInteraction error
        newInteraction()
        self.call_view(self.gadt, "view")
        endInteraction()
        self.assertEqual(len(logged_actions), 0)
        # # EDIT
        # check organisation edit
        logged_actions[:] = []  # clear
        self.call_view(self.armeedeterre, "@@edit")
        self.assertEqual(len(logged_actions), 0)
        # check sub organization edit
        logged_actions[:] = []  # clear
        self.call_view(self.brigadelh, "@@edit")
        self.assertEqual(len(logged_actions), 0)
        # check person edit
        logged_actions[:] = []  # clear
        self.call_view(self.degaulle, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle " "CTX_PATH=/mydirectory/degaulle CASE=contact_edit")
        # check position edit
        logged_actions[:] = []  # clear
        self.call_view(self.general_adt, "@@edit")
        self.assertEqual(len(logged_actions), 0)
        # check held_position edit
        logged_actions[:] = []  # clear
        # necessary for z3c.formwidget.query widget initialization... to avoid NoInteraction error
        newInteraction()
        self.call_view(self.gadt, "@@edit")
        endInteraction()
        self.assertEqual(len(logged_actions), 0)
        # # OVERLAY
        # check directory overlay
        logged_actions[:] = []
        self.call_view(self.mydirectory, "view")
        self.assertEqual(len(logged_actions), 0)
        # simulate overlay
        self.armeedeterre.REQUEST["HTTP_REFERER"] = "http://nohost/plone/mydirectory"
        self.armeedeterre.REQUEST["ajax_load"] = "12345678"
        self.call_view(self.degaulle, "view")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle " "CTX_PATH=/mydirectory CASE=contact_overlay")

    def test_get_object_from_referer(self):
        portal = self.portal
        url = self.armeedeterre.absolute_url()
        self.assertEqual(get_object_from_referer(portal, url), self.armeedeterre)
        # views and parameters are removed
        self.assertEqual(get_object_from_referer(portal, url + "/@@edit?_authenticator=123"), self.armeedeterre)
        self.assertEqual(get_object_from_referer(portal, url + "/++add++organization"), self.armeedeterre)
        self.assertEqual(get_object_from_referer(portal, url + "/++add++position?x=1"), self.armeedeterre)
        # on a view like organization/view
        self.assertEqual(get_object_from_referer(portal, url + "/view"), self.armeedeterre)
        # on a method of an object, like held_position/edit (org selection on held_position edit)
        self.assertEqual(get_object_from_referer(portal, self.gadt.absolute_url() + "/edit"), self.gadt)
        # not found
        self.assertIsNone(get_object_from_referer(portal, portal.absolute_url() + "/mydirectory/unknown"))
        self.assertEqual(get_object_from_referer(portal, portal.absolute_url() + "/unknown", default="x"), "x")

    def test_get_object_from_request(self):
        request = self.portal.REQUEST
        # published object
        request["PUBLISHED"] = self.corpsa
        self.assertEqual(get_object_from_request(request), self.corpsa)
        # published view
        request["PUBLISHED"] = self.armeedeterre.restrictedTraverse("view")
        self.assertEqual(get_object_from_request(request, portal=self.portal), self.armeedeterre)
        # nothing published or portal: the referer is used
        request["PUBLISHED"] = None
        request["HTTP_REFERER"] = self.corpsa.absolute_url() + "/@@edit?_authenticator=123"
        self.assertEqual(get_object_from_request(request), self.corpsa)
        request["PUBLISHED"] = self.portal.restrictedTraverse("view")
        self.assertEqual(get_object_from_request(request), self.corpsa)
        request["HTTP_REFERER"] = self.portal.absolute_url() + "/unknown"
        self.assertEqual(get_object_from_request(request, default="x"), "x")

    def test_get_valid_url(self):
        self.assertEqual(get_valid_url("www.imio.be"), "http://www.imio.be")
        self.assertEqual(get_valid_url("http://www.imio.be"), "http://www.imio.be")
        self.assertEqual(get_valid_url("https://www.imio.be"), "https://www.imio.be")
        self.assertEqual(get_valid_url(""), "")
        self.assertIsNone(get_valid_url(None))

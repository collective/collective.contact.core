# -*- coding: utf8 -*-
from collective.contact.core import logged_actions
from collective.contact.core.testing import FUNCTIONAL
from ecreall.helpers.testing.base import BaseTest
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from zope.security.management import endInteraction
from zope.security.management import newInteraction

import unittest


def rmv_uid(idx):
    return logged_actions[idx][logged_actions[idx].index(" PATH=") + 1:]


class TestBrowserUtils(unittest.TestCase, BaseTest):

    layer = FUNCTIONAL

    def setUp(self):
        super(TestBrowserUtils, self).setUp()
        self.login(TEST_USER_NAME)
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        mydirectory = self.portal['mydirectory']
        self.degaulle = mydirectory['degaulle']
        self.adt = self.degaulle['adt']
        self.gadt = self.degaulle['gadt']
        self.pepper = mydirectory['pepper']
        self.sergent_pepper = self.pepper['sergent_pepper']
        self.rambo = mydirectory['rambo']
        self.armeedeterre = mydirectory['armeedeterre']
        self.corpsa = self.armeedeterre['corpsa']
        self.divisionalpha = self.corpsa['divisionalpha']
        self.regimenth = self.divisionalpha['regimenth']
        self.brigadelh = self.regimenth['brigadelh']
        self.general_adt = self.armeedeterre['general_adt']
        self.sergent_lh = self.brigadelh['sergent_lh']
        self.draper = mydirectory['draper']
        self.captain_crunch = self.draper['captain_crunch']
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
        api.portal.set_registry_record("collective.contact.core.interfaces.IContactCoreParameters."
                                       "audit_contact_access", True)
        api.portal.set_registry_record("collective.contact.core.interfaces.IContactCoreParameters.audit_contact_types",
                                       [])
        # # VIEW
        # check organisation view
        self.call_view(self.armeedeterre, "view")
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre "
                                     "CTX_PATH=/mydirectory/armeedeterre CASE=contact_view")
        self.assertEqual(rmv_uid(1), "PATH=/mydirectory/degaulle/adt "
                                     "CTX_PATH=/mydirectory/armeedeterre CASE=contact_view")
        # check sub organization view
        logged_actions[:] = []  # clear
        self.call_view(self.brigadelh, "view")
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh "
                                     "CTX_PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh"
                                     " CASE=contact_view")
        self.assertEqual(rmv_uid(1), "PATH=/mydirectory/rambo/brigadelh "
                                     "CTX_PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh"
                                     " CASE=contact_view")
        # check person view
        logged_actions[:] = []  # clear
        self.call_view(self.degaulle, "view")
        self.assertEqual(len(logged_actions), 5)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        self.assertEqual(rmv_uid(1), "PATH=/mydirectory/degaulle/adt "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        self.assertEqual(rmv_uid(2), "PATH=/mydirectory/armeedeterre "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        self.assertEqual(rmv_uid(3), "PATH=/mydirectory/degaulle/gadt "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        self.assertEqual(rmv_uid(4), "PATH=/mydirectory/armeedeterre "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
        # check position view
        logged_actions[:] = []  # clear
        self.call_view(self.general_adt, "view")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre/general_adt "
                                     "CTX_PATH=/mydirectory/armeedeterre/general_adt CASE=contact_view")
        # check held_position view
        logged_actions[:] = []  # clear
        # necessary for z3c.formwidget.query widget initialization... to avoid NoInteraction error
        newInteraction()
        self.call_view(self.gadt, "view")
        endInteraction()
        self.assertEqual(len(logged_actions), 2)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre/general_adt "
                                     "CTX_PATH=/mydirectory/degaulle/gadt CASE=contact_view")
        self.assertEqual(rmv_uid(1), "PATH=/mydirectory/degaulle/gadt "
                                     "CTX_PATH=/mydirectory/degaulle/gadt CASE=contact_view")
        # # EDIT
        # check organisation edit
        logged_actions[:] = []  # clear
        self.call_view(self.armeedeterre, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre "
                                     "CTX_PATH=/mydirectory/armeedeterre CASE=contact_edit")
        # check sub organization edit
        logged_actions[:] = []  # clear
        self.call_view(self.brigadelh, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh "
                                     "CTX_PATH=/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh"
                                     " CASE=contact_edit")
        # check person edit
        logged_actions[:] = []  # clear
        self.call_view(self.degaulle, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_edit")
        # check position edit
        logged_actions[:] = []  # clear
        self.call_view(self.general_adt, "@@edit")
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre/general_adt "
                                     "CTX_PATH=/mydirectory/armeedeterre/general_adt CASE=contact_edit")
        # check held_position edit
        logged_actions[:] = []  # clear
        # necessary for z3c.formwidget.query widget initialization... to avoid NoInteraction error
        newInteraction()
        self.call_view(self.gadt, "@@edit")
        endInteraction()
        self.assertEqual(len(logged_actions), 1)
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle/gadt "
                                     "CTX_PATH=/mydirectory/degaulle/gadt CASE=contact_edit")
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
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/armeedeterre "
                                     "CTX_PATH=/mydirectory CASE=contact_overlay")
        self.assertEqual(rmv_uid(1), "PATH=/mydirectory/degaulle/adt "
                                     "CTX_PATH=/mydirectory CASE=contact_overlay")
        # # # we filter on person only
        api.portal.set_registry_record("collective.contact.core.interfaces.IContactCoreParameters.audit_contact_types",
                                       ["person"])
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
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_view")
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
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle "
                                     "CTX_PATH=/mydirectory/degaulle CASE=contact_edit")
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
        self.assertEqual(rmv_uid(0), "PATH=/mydirectory/degaulle "
                                     "CTX_PATH=/mydirectory CASE=contact_overlay")

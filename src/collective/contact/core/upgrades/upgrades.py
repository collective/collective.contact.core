# -*- coding: utf-8 -*-

from plone import api

from ecreall.helpers.upgrade.interfaces import IUpgradeTool


def v2(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.core.upgrades:v2')
    catalog = api.portal.get_tool(name='portal_catalog')
    catalog.clearFindAndRebuild()

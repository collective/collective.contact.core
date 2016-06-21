# -*- coding: utf-8 -*-

from zc.relation.interfaces import ICatalog
from z3c.relationfield.event import updateRelations
from z3c.relationfield.interfaces import IHasRelations
from zope.component import getUtility

from plone import api

from collective.contact.widget.interfaces import IContactContent
from ecreall.helpers.upgrade.interfaces import IUpgradeTool

from ..content.held_position import IHeldPosition


def reindex_relations(context):
    """Clear the relation catalog to fix issues with interfaces that don't exist anymore.
    This actually fixes the from_interfaces_flattened and to_interfaces_flattened indexes.
    """
    rcatalog = getUtility(ICatalog)
    rcatalog.clear()
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog.searchResults(object_provides=IHasRelations.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        updateRelations(obj, None)


def v2(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.core.upgrades:v2')
    catalog = api.portal.get_tool(name='portal_catalog')
    catalog.clearFindAndRebuild()
    reindex_relations(context)


def v3(context):
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides=IContactContent.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        obj.is_created = True


def v4(context):
    IUpgradeTool(context).runImportStep('collective.contact.core', 'rolemap')


def v5(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.widget:default')
    # add sortable_title column and reindex persons and organizations
    tool.addMetadata('sortable_title')
    tool.reindexContents(IContactContent, ('sortable_title',))


def v6(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.core.upgrades:v6')
    tool.refreshResources()


def v7(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.core.upgrades:v7')


def v8(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.core.upgrades:v8')


def v9(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.core.upgrades:v9')


def v10(context):
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog.searchResults(object_provides=IHeldPosition.__identifier__)
    for brain in brains:
        brain.getObject().reindexObject(['start', 'end'])

# -*- coding: utf-8 -*-
from collective.contact.core.interfaces import IContactCoreParameters
from collective.contact.core.interfaces import IHeldPosition
from collective.contact.widget.interfaces import IContactContent
from plone import api
from Products.CMFPlone.utils import base_hasattr
from z3c.relationfield.event import updateRelations
from z3c.relationfield.interfaces import IHasRelations
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName


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


def refreshResources(self):
    """Refresh all resource registries
    """
    css_tool = getToolByName(self.portal, 'portal_css')
    css_tool.cookResources()

    js_tool = getToolByName(self.portal, 'portal_javascripts')
    js_tool.cookResources()

    kss_tool = getToolByName(self.portal, 'portal_kss', None)
    if kss_tool:
        kss_tool.cookResources()

    return "Js, kss and css refreshed"


def v2(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core.upgrades:v2',
        purge_old=False,
    )
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
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'rolemap',
    )


def v5(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.widget:default',
    )
    # add sortable_title column and reindex persons and organizations
    catalog = api.portal.get_tool('portal_catalog')
    catalog.addColumn('sortable_title')
    items = api.content.find(
        object_provides='collective.contact.widget.interfaces.IContactContent'
    )
    for item in items:
        item.getObject().reindexObject(idxs=['sortable_title']
    )


def v6(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core.upgrades:v6',
    )
    refreshResources()


def v7(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core.upgrades:v7',
    )


def v8(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core.upgrades:v8',
    )


def v9(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core.upgrades:v9',
    )


def v10(context):
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog.searchResults(object_provides=IHeldPosition.__identifier__)
    for brain in brains:
        brain.getObject().reindexObject(['start', 'end'])


def v11(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'typeinfo',
    )
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'plone.app.registry',
    )
    val = api.portal.get_registry_record(name='person_contact_details_private', interface=IContactCoreParameters)
    if val is None:
        api.portal.set_registry_record(name='person_contact_details_private', value=True,
                                       interface=IContactCoreParameters)


def v12(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'plone.app.registry',
    )
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides=IContactContent.__identifier__)
    for brain in brains:
        brain.getObject().reindexObject(['Title', 'sortable_title', 'get_full_title', 'SearchableText'])


def v13(context):
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog.unrestrictedSearchResults(object_provides=IContactContent.__identifier__)
    for brain in brains:
        obj = brain.getObject()
        if base_hasattr(obj, 'is_created'):
            delattr(obj, 'is_created')


def v14(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'plone.app.registry', 'typeinfo'
    )


def v15(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'plone.app.registry',
    )
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'catalog'
    )
    items = api.content.find(
        object_provides='collective.contact.widget.interfaces.IContactContent'
    )
    for item in items:
        item.getObject().reindexObject(idxs=['email'])

def v16(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'plone.app.registry',
    )
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'catalog'
    )
    items = api.content.find(
        object_provides='collective.contact.widget.interfaces.IContactContent'
    )
    for item in items:
        item.getObject().reindexObject(idxs=['email', 'contact_source'])


def refresh_resources_registry(context):
    context.runAllImportStepsFromProfile(
        'profile-collective.contact.core', 'plone.app.registry',
    )

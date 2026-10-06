# coding=utf-8
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.content.directory import IDirectory
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.person import IPerson
from collective.contact.core.content.position import IPosition
from collective.contact.core.interfaces import IContactCoreParameters
from collective.contact.core.interfaces import IHeldPosition
from collective.contact.widget.interfaces import IContactContent
from plone import api
from plone.app.iterate.interfaces import IWorkingCopy
from plone.registry.interfaces import IRecordModifiedEvent
from z3c.form.interfaces import NO_VALUE
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.container.contained import ContainerModifiedEvent
from zope.intid.interfaces import IIntIds
from zope.schema import getFields

# update indexes of related content when a content is modified
# you can monkey patch this value if you have an index that needs this
indexes_to_update = ['SearchableText']


def update_related_with_held_position(obj, event=None):
    """Reindexes related person `SearchableText`."""
    if isinstance(event, ContainerModifiedEvent):
        return

    obj.get_person().reindexObject(idxs=indexes_to_update)


def update_related_with_position(obj, event=None):
    """Reindexes related held_position `SearchableText` and related hp person `SearchableText`."""
    if isinstance(event, ContainerModifiedEvent):
        return

    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)
        update_related_with_held_position(held_position)


def update_related_with_person(obj, event=None):
    """Reindexes contained held_positions `SearchableText`."""
    if isinstance(event, ContainerModifiedEvent):
        return

    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)


def update_related_with_organization(obj, event=None):
    """Reindexes related hp, person, position `SearchableText` and identically the contained organizations."""
    if isinstance(event, ContainerModifiedEvent):
        return

    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)
        update_related_with_held_position(held_position)

    for position in obj.get_positions():
        position.reindexObject(idxs=indexes_to_update)
        for held_position in position.get_held_positions():
            held_position.reindexObject(idxs=indexes_to_update)
            update_related_with_held_position(held_position)

    for child in list(obj.values()):
        if IOrganization.providedBy(child):
            child.reindexObject(idxs=indexes_to_update)
            update_related_with_organization(child)


def referenceObjectRemoved(obj, event):
    """Unindex relations on a deleted contact content."""
    allowed_interfaces = (IDirectory, IOrganization, IPerson, IHeldPosition, IPosition)
    if not any(i.providedBy(obj) for i in allowed_interfaces):
        return
    # Avoid an error when we try to remove a working copy (plone.app.iterate)
    if IWorkingCopy.providedBy(obj):
        return

    intids = getUtility(IIntIds)
    try:
        int_id = intids.getId(obj)
    except KeyError:
        return
    catalog = getUtility(ICatalog)
    outcoming_rels = catalog.findRelations({"from_id": int_id})
    for rel in list(outcoming_rels):
        catalog.unindex(rel)
    incoming_rels = catalog.findRelations({"to_id": int_id})
    for rel in list(incoming_rels):
        catalog.unindex(rel)


def clear_fields_use_parent_address(obj, event):
    """Deletes use_parent_address slave fields if upa is selected."""
    if obj.use_parent_address and obj.use_parent_address != NO_VALUE:
        upa_field = getFields(IContactDetails)['use_parent_address']
        slave_ids = [f['name'] for f in upa_field.slave_fields]
        for field_name in slave_ids:
            try:
                delattr(obj, field_name)
            except AttributeError:
                pass


def recordModified(event):
    """Handles configuration change.
    Updates `contact_source` index after `contact_source_metadata_content` change.
    """
    if IRecordModifiedEvent.providedBy(event) \
            and event.record.interfaceName \
            and event.record.interface == IContactCoreParameters:
        if event.record.fieldName == 'contact_source_metadata_content':
            pc = api.portal.get_tool('portal_catalog')
            for brain in pc(object_provides=IContactContent.__identifier__):
                brain.getObject().reindexObject(idxs=['contact_source'])

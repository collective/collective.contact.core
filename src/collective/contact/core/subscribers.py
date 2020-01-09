from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.person import IPerson
from collective.contact.core.content.position import IPosition
from collective.contact.core.interfaces import IHeldPosition
from z3c.form.interfaces import NO_VALUE
from zope.container.contained import ContainerModifiedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema import getFields


# update indexes of related content when a content is modified
# you can monkey patch this value if you have an index that needs this
indexes_to_update = ['SearchableText']


def update_related_with_held_position(obj, event=None):
    if isinstance(event, ContainerModifiedEvent):
        return

    obj.get_person().reindexObject(idxs=indexes_to_update)


def update_related_with_position(obj, event=None):
    if isinstance(event, ContainerModifiedEvent):
        return

    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)
        update_related_with_held_position(held_position)


def update_related_with_person(obj, event=None):
    if isinstance(event, ContainerModifiedEvent):
        return

    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)


def update_related_with_organization(obj, event=None):
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

    for child in obj.values():
        if IOrganization.providedBy(child):
            child.reindexObject(idxs=indexes_to_update)
            update_related_with_organization(child)


def clear_fields_use_parent_address(obj, event):
    """If 'use parent address' has been selected,
    ensure content address fields are cleared
    """
    if obj.use_parent_address and obj.use_parent_address != NO_VALUE:
        upa_field = getFields(IContactDetails)['use_parent_address']
        slave_ids = [f['name'] for f in upa_field.slave_fields]
        for field_name in slave_ids:
            try:
                delattr(obj, field_name)
            except AttributeError:
                pass

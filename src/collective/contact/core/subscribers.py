from five import grok

from zope.lifecycleevent.interfaces import IObjectAddedEvent,\
    IObjectCreatedEvent, IObjectModifiedEvent

from collective.contact.widget.interfaces import IContactContent
from collective.contact.core.content.held_position import IHeldPosition
from collective.contact.core.content.position import IPosition
from collective.contact.core.content.person import IPerson
from collective.contact.core.content.organization import IOrganization


@grok.subscribe(IContactContent, IObjectAddedEvent)
def set_is_created(obj, event):
    obj.is_created = True


# update indexes of related content when a content is modified

indexes_to_update = ['SearchableText']

@grok.subscribe(IHeldPosition, IObjectCreatedEvent)
@grok.subscribe(IHeldPosition, IObjectModifiedEvent)
def update_related_with_held_position(obj):
    obj.get_person().reindexObject(idxs=indexes_to_update)


@grok.subscribe(IPosition, IObjectModifiedEvent)
def update_related_with_position(obj):
    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)
        update_related_with_held_position(held_position)


@grok.subscribe(IPerson, IObjectModifiedEvent)
def update_related_with_person(obj):
    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)


@grok.subscribe(IOrganization, IObjectModifiedEvent)
def update_related_with_organization(obj):
    for held_position in obj.get_held_positions():
        held_position.reindexObject(idxs=indexes_to_update)
        update_related_with_held_position(held_position)

    for position in obj.get_positions():
        position.reindexObject(idxs=indexes_to_update)
        for held_position in position.get_held_positions():
            held_position.reindexObject(idxs=indexes_to_update)
            update_related_with_held_position(held_position)


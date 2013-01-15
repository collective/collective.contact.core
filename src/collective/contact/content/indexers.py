from plone.indexer import indexer

from collective.contact.content.content.held_position import IHeldPosition
from collective.contact.content.content.organization import IOrganization


@indexer(IOrganization)
def organization_searchable_text(obj):
    return ' '.join(obj.get_organizations_titles())


@indexer(IHeldPosition)
def held_position_searchable_text(obj):
    indexed_fields = []
    indexed_fields.append(obj.get_person().Title())
    position = obj.get_position()
    if position is not None:
        indexed_fields.append(position.Title())
    organization = obj.get_organization()
    indexed_fields.extend(organization.get_organizations_titles())
    return ' '.join(indexed_fields)

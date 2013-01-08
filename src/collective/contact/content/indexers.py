from plone.indexer import indexer

from collective.contact.content.held_position import IHeldPosition
from collective.contact.content.organization import IOrganization


@indexer(IOrganization)
def organization_searchable_text(obj):
    return ' '.join(obj.get_full_title())


@indexer(IHeldPosition)
def held_position_searchable_text(obj):
    indexed_fields = []
    position_or_organization = obj.position.to_object
    if position_or_organization.portal_type == 'position':
        position = position_or_organization
        indexed_fields.append(position.Title())
        organization = position.getParentNode()
    elif position_or_organization.portal_type == 'organization':
        organization = position_or_organization
    indexed_fields.extend(organization.get_full_title())
    return ' '.join(indexed_fields)

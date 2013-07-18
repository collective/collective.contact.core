from plone.indexer import indexer

from collective.contact.core.content.held_position import IHeldPosition
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.position import IPosition
from collective.contact.core.content.person import IPerson
from collective.contact.core.behaviors import IRelatedOrganizations

def ensure_unicode(x):
    if not isinstance(x, unicode):
        x = unicode(x, 'utf-8', 'ignore')
    return x


@indexer(IOrganization)
def organization_searchable_text(organization):
    text = ''
    if IRelatedOrganizations.providedBy(organization) \
            and organization.related_organizations is not None:
        for related in organization.related_organizations:
            text += u' '.join(related.to_object.get_organizations_titles())

    text += u' '.join(organization.get_organizations_titles())
    return text


@indexer(IHeldPosition)
def held_position_searchable_text(obj):
    indexed_fields = []
    indexed_fields.append(obj.get_person().get_title())
    position = obj.get_position()
    if position is not None:
        indexed_fields.append(position.title)

    organization = obj.get_organization()
    indexed_fields.extend(organization.get_organizations_titles())
    return u' '.join(indexed_fields)


@indexer(IPosition)
def position_searchable_text(obj):
    return ensure_unicode(obj.SearchableText()) + ensure_unicode(obj.get_organization().Title())


@indexer(IPerson)
def person_searchable_text(obj):
    results = []
    results.append(ensure_unicode(obj.SearchableText()))
    for held_positions in obj.get_held_positions():
        results.append(ensure_unicode(held_position_searchable_text(held_positions)()))
    return results

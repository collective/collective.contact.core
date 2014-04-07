from plone.indexer import indexer
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import safe_unicode

from collective.contact.core.content.held_position import IHeldPosition
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.position import IPosition
from collective.contact.core.content.person import IPerson
from collective.contact.core.behaviors import IRelatedOrganizations


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

    if obj.label:
        indexed_fields.append(obj.label)

    return u' '.join(indexed_fields)


@indexer(IPosition)
def position_searchable_text(obj):
    return u"%s %s" % (safe_unicode(obj.SearchableText()),
                       safe_unicode(obj.get_organization().Title()))


@indexer(IPerson)
def person_searchable_text(obj):
    results = []
    results.append(safe_unicode(obj.SearchableText()))
    for held_positions in obj.get_held_positions():
        results.append(held_position_searchable_text(held_positions)())
    return results


@indexer(IPerson)
def person_sortable_title(obj):
    if obj.firstname is None:
        fullname = obj.lastname
    else:
        fullname = u"%s %s" % (obj.lastname, obj.firstname)

    return normalizeString(fullname, context=obj)


@indexer(IHeldPosition)
def held_position_sortable_title(obj):
    sortable_fullname = person_sortable_title(obj.get_person())()
    held_position_title = obj.Title()
    return u"%s-%s" % (sortable_fullname,
                       normalizeString(safe_unicode(held_position_title),
                                       context=obj))

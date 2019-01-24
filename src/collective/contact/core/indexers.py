from datetime import date
from plone import api
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_unicode

from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.position import IPosition
from collective.contact.core.content.person import IPerson
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.behaviors import IRelatedOrganizations
from collective.contact.core.interfaces import IHeldPosition


@indexer(IOrganization)
def organization_searchable_text(organization):
    words = []
    if IRelatedOrganizations.providedBy(organization) \
            and organization.related_organizations is not None:
        for related in organization.related_organizations:
            words += related.to_object.get_organizations_titles()

    words += organization.get_organizations_titles()

    email = IContactDetails(organization).email
    if email:
        words.append(email)

    return u' '.join(words)


@indexer(IHeldPosition)
def held_position_searchable_text(obj):
    indexed_fields = []
    indexed_fields.append(obj.get_person().get_title())
    position = obj.get_position()
    if position is not None:
        indexed_fields.append(position.title)

    organization = obj.get_organization()
    if organization:
        indexed_fields.extend(organization.get_organizations_titles())

    label = obj.get_label()
    if label:
        indexed_fields.append(label)

    email = IContactDetails(obj).email
    if email:
        indexed_fields.append(email)

    return u' '.join(indexed_fields)


@indexer(IPosition)
def position_searchable_text(obj):
    result = [safe_unicode(obj.SearchableText())]
    result.append(safe_unicode(obj.get_organization().Title()))
    email = IContactDetails(obj).email
    if email:
        result.append(email)
    return u' '.join(result)


@indexer(IPerson)
def person_searchable_text(obj):
    results = []
    use_description = api.portal.get_registry_record(
        "collective.contact.core.interfaces.IContactCoreParameters."
        "use_description_to_search_person")
    if use_description:
        text = obj.SearchableText()
    else:
        text = obj.Title()

    results.append(safe_unicode(text))

    email = IContactDetails(obj).email
    if email:
        results.append(email)

    use_held_positions = api.portal.get_registry_record(
        "collective.contact.core.interfaces.IContactCoreParameters."
        "use_held_positions_to_search_person")
    if use_held_positions:
        for held_positions in obj.get_held_positions():
            results.append(held_position_searchable_text(held_positions)())
    return results


@indexer(IPerson)
def person_sortable_title(obj):
    return obj.get_sortable_title()


@indexer(IHeldPosition)
def held_position_sortable_title(obj):
    return obj.get_sortable_title()


@indexer(IHeldPosition)
def start_date(obj):
    if obj.start_date:
        return obj.start_date
    # if empty, we return creation date
    return obj.created()


@indexer(IHeldPosition)
def end_date(obj):
    if obj.end_date:
        return obj.end_date
    # if empty we return future date
    return date(2100, 01, 01)

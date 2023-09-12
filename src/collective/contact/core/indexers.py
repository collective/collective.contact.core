# -*- coding: utf-8 -*-

from collective.contact.core.behaviors import ADDRESS_FIELDS
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.behaviors import IRelatedOrganizations
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.person import IPerson
from collective.contact.core.content.position import IPosition
from collective.contact.core.interfaces import IContactable
from collective.contact.core.interfaces import IHeldPosition
from collective.contact.widget.interfaces import IContactContent
from collective.dexteritytextindexer.converters import DefaultDexterityTextIndexFieldConverter
from collective.dexteritytextindexer.interfaces import IDynamicTextIndexExtender
from datetime import date
from plone import api
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapts
from zope.interface import implements


@indexer(IContactContent)
def contact_email(contact):
    email = IContactDetails(contact).email
    return email.lower() or u''


@indexer(IContactContent)
def contact_source(contact):
    csmc = api.portal.get_registry_record('collective.contact.core.interfaces.IContactCoreParameters.'
                                          'contact_source_metadata_content', default=u'{gft}')
    variables = {'gft': contact.get_full_title()}
    contactable = IContactable(contact)
    details = contactable.get_contact_details()
    address = details.pop('address')
    for fld in ADDRESS_FIELDS:
        address.setdefault(fld, '')
    variables.update(address)
    variables.update(details)
    try:
        return csmc.format(**variables)
    except Exception:
        pass
    return u''


class OrganizationSearchableExtender(object):
    """Extends SearchableText of an organization."""
    adapts(IOrganization)
    implements(IDynamicTextIndexExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        words = []
        organization = self.context
        if IRelatedOrganizations.providedBy(organization) \
                and organization.related_organizations is not None:
            for related in organization.related_organizations:
                words += related.to_object.get_organizations_titles()

        words += organization.get_organizations_titles()

        if organization.enterprise_number is not None:
            words.append(organization.enterprise_number)

        email = IContactDetails(organization).email
        if email:
            words.append(email)

        return u' '.join(words)


class HeldPositionSearchableExtender(object):
    """Extends SearchableText of a held position."""
    adapts(IHeldPosition)
    implements(IDynamicTextIndexExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        obj = self.context
        indexed_fields = [obj.get_person().get_title()]
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


class PositionSearchableExtender(object):
    """Extends SearchableText of a position."""
    adapts(IPosition)
    implements(IDynamicTextIndexExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        obj = self.context
        result = [safe_unicode(obj.get_organization().Title())]
        email = IContactDetails(obj).email
        if email:
            result.append(email)
        return u' '.join(result)


class PersonSearchableExtender(object):
    """Extends SearchableText of a position."""
    adapts(IPerson)
    implements(IDynamicTextIndexExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        obj = self.context
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
                results.append(HeldPositionSearchableExtender(held_positions)())
        return u' '.join(results)


class ContactEscapingTitleFieldConverter(DefaultDexterityTextIndexFieldConverter):
    """Contact field converter for collective.dexteritytextindexer to escape title and description."""

    def convert(self):
        """Convert the adapted field value to text/plain for indexing"""
        if self.field.__name__ in ('title', 'description'):
            return ''
        return super(ContactEscapingTitleFieldConverter, self).convert()


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
    return date(2100, 1, 1)

from Acquisition import aq_base

from five import grok
from plone import api

from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.browser import TEMPLATES_DIR
from collective.contact.core.behaviors import ADDRESS_FIELDS
from collective.contact.core.interfaces import IHeldPosition, IContactCoreParameters

grok.templatedir(TEMPLATES_DIR)


def get_address(obj):
    """Returns a dictionary which contains address fields"""
    if aq_base(obj).use_parent_address is True:
        related = None
        priv = api.portal.get_registry_record(name='person_contact_details_private', interface=IContactCoreParameters)
        if IHeldPosition.providedBy(obj) and priv:
            # For a held position, we use the related element: a position or an organization
            related = (obj.get_position() or obj.get_organization())
        elif hasattr(obj, 'aq_parent'):
            related = obj.aq_parent

        if related and IContactDetails.providedBy(related):
            return get_address(related)
        else:
            return {}

    address = {}
    address_fields = ADDRESS_FIELDS
    obj = aq_base(obj)
    for field in address_fields:
        value = getattr(obj, field, '') or ''
        address[field] = value

    if not [v for v in address.values() if v]:
        # no value in address fields
        return {}

    return address


class Address(grok.View):
    grok.name('address')
    grok.context(IContactDetails)
    grok.require("zope2.View")
    grok.template('address')

    def namespace(self):
        return get_address(self.context)

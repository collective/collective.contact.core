from Acquisition import aq_base

from five import grok

from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.browser import TEMPLATES_DIR


grok.templatedir(TEMPLATES_DIR)


def get_address(obj):
    """Returns a dictionary which contains address fields"""
    address = {}
    if aq_base(obj).use_parent_address is True and IContactDetails.providedBy(obj.aq_parent):
        address = get_address(obj.aq_parent)
        if address:
            return address

    address_fields = ['country', 'region', 'zip_code',
                      'city', 'street', 'number',
                      'additional_address_details']
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

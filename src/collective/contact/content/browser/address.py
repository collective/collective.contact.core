from Acquisition import aq_base

from five import grok

from collective.contact.content.behaviors import IContactDetails
from collective.contact.content.browser import TEMPLATES_DIR


grok.templatedir(TEMPLATES_DIR)


def get_address(obj):
    """Returns a dictionary which contains address fields"""
    address = {}
    address_fields = ['country', 'region', 'zip_code',
                      'city', 'street', 'number',
                      'additional_address_details']
    if obj is None:
        return dict([(x, '') for x in address_fields])
        # OR dict(zip(address_fields, ['']*len(address_fields)))
    obj = aq_base(obj)
    for field in address_fields:
        value = getattr(obj, field, '') or ''
        address[field] = value
    return address


class Address(grok.View):
    grok.name('address')
    grok.context(IContactDetails)
    grok.require("zope2.View")
    grok.template('address')

    def namespace(self):
        return get_address(self.context)

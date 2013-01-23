import os.path

from zope.globalrequest import getRequest
from five import grok
from Acquisition import aq_base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.dexterity.browser.view import DefaultView
from plone.dexterity.utils import getAdditionalSchemata

from collective.contact.content.browser import TEMPLATES_DIR
from collective.contact.content.browser.address import get_address
from collective.contact.content.behaviors import IContactDetails
from collective.contact.content.interfaces import IContactContent, IContactable


class Contactable(grok.Adapter):
    """Base adapter class for objects that have the IContactDetails behavior fields"""
    grok.provides(IContactable)
    grok.context(IContactContent)
    grok.baseclass()

    @property
    def person(self):
        return None

    @property
    def position(self):
        return None

    @property
    def organizations(self):
        return []

    def _get_contactables(self):
        """Build a list of objects which have the IContactDetails behavior
        for each contact information (email, phone, ...)
        we use the one of the first object in this list which have this information
        """
        contactables = []
        if self.person is not None:
            contactables.append(self.person)
        if self.position is not None:
            contactables.append(self.position)
        if self.organizations:
            contactables.extend(reversed(self.organizations))
        return contactables

    def _get_address(self):
        # search the object that carries the address
        for obj in self._get_contactables():
            obj = aq_base(obj)
            city = getattr(obj, 'city', '') or ''
            street = getattr(obj, 'street', '') or ''
            if city and street:
                return get_address(obj)
        return {}

    def get_contact_details(self):
        contact_details = {}
        contact_details_fields = ['email', 'phone', 'cell_phone', 'im_handle']
        for field in contact_details_fields:
            # search the object that carries the field
            for obj in self._get_contactables():
                obj = aq_base(obj)
                value = getattr(obj, field, '') or ''
                if value:
                    contact_details[field] = value
                    break
            else:
                contact_details[field] = ''
        contact_details['address'] = self._get_address()
        return contact_details

    def get_parent_address(self):
        address = self._get_address()
        if not address:
            return ''
        template_path = os.path.join(TEMPLATES_DIR, 'address.pt')
        template = ViewPageTemplateFile(template_path)
        self.request = getRequest()
        return template(self, address)


class BaseView(DefaultView):

    @property
    def additionalSchemata(self):
        # we don't want IContactDetails in behaviors
        additional_schemata = list(getAdditionalSchemata(context=self.context))
        if IContactDetails in additional_schemata:
            additional_schemata.remove(IContactDetails)
        return additional_schemata

    def render_address(self):
        template_path = os.path.join(TEMPLATES_DIR, 'address.pt')
        template = ViewPageTemplateFile(template_path)
        return template(self, self.address)

import os.path

from zope.globalrequest import getRequest
from zope.interface import Interface
from five import grok
from Acquisition import aq_base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.dexterity.browser.view import DefaultView
from plone.dexterity.utils import getAdditionalSchemata

from collective.contact.core.browser import TEMPLATES_DIR
from collective.contact.core.browser.address import get_address
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.interfaces import IContactable
from collective.contact.widget.interfaces import IContactContent
from collective.contact.core.behaviors import CONTACT_DETAILS_FIELDS
from collective.contact.core.browser.utils import get_valid_url


grok.templatedir(TEMPLATES_DIR)


class ContactDetailsContactable(grok.Adapter):
    """Common adapter class for objects that just implement the IContactDetails behavior"""
    grok.provides(IContactable)
    grok.context(Interface)

    def get_contact_details(self, keys=(), fallback=True):
        if not IContactDetails.providedBy(self.context):
            raise TypeError("Your contactable content must provide IContactDetails "
                            "if it doesn't have a more specific contactable adapter")

        contact_details = {}
        if keys:
            contact_details_fields = [k for k in keys if k != 'address']
        else:
            contact_details_fields = CONTACT_DETAILS_FIELDS

        context = aq_base(self.context)
        for field in contact_details_fields:
            # search the object that carries the field
            value = getattr(context, field, '') or ''
            contact_details[field] = value

        if (not keys) or ('address' in keys):
            contact_details['address'] = get_address(context)

        if 'website' in contact_details:
            contact_details['website'] = get_valid_url(
                contact_details['website'])

        return contact_details

    def get_parent_address(self):
        return u""


class ContactDetails(grok.View):
    grok.name('contactdetails')
    grok.template('contactdetails')
    grok.context(IContactContent)

    template_path = os.path.join(TEMPLATES_DIR, 'address.pt')

    def update(self):
        contactable = IContactable(self.context)
        self.contact_details = contactable.get_contact_details()

    def render_address(self):
        template = ViewPageTemplateFile(self.template_path)
        return template(self, self.contact_details['address'])


class NoFallbackContactDetails(ContactDetails):
    grok.name('nofallbackcontactdetails')

    def update(self):
        contactable = IContactable(self.context)
        self.contact_details = contactable.get_contact_details(fallback=False)


class Contactable(grok.Adapter):
    """Base adapter class for contact content types with fallback system"""
    grok.provides(IContactable)
    grok.context(IContactContent)
    grok.baseclass()

    @property
    def person(self):
        return None

    def held_position(self):
        return None

    @property
    def position(self):
        return None

    @property
    def organizations(self):
        return []

    def _get_contactables(self):
        """
        Build a list of objects which have the IContactDetails behavior
        for each contact information (email, phone, ...)
        we use the one of the first object in this list which have this information
        """
        contactables = []
        related_items = [self.context, self.held_position, self.person, self.position] + list(reversed(self.organizations))
        for related_item in related_items:
            if related_item is not None \
               and IContactDetails.providedBy(related_item) \
               and related_item not in contactables:
                contactables.append(related_item)

        return contactables

    def _get_address(self, contactables):
        for obj in contactables:
            address = get_address(obj)
            if address:
                return address

        return {}

    def get_contact_details(self, keys=(), fallback=True):
        contact_details = {}
        if keys:
            contact_details_fields = [k for k in keys if k != 'address']
        else:
            contact_details_fields = CONTACT_DETAILS_FIELDS

        if fallback:
            contactables = self._get_contactables()
        else:
            contactables = [self.context]

        for field in contact_details_fields:
            # search the object that carries the field
            for obj in contactables:
                obj = aq_base(obj)
                value = getattr(obj, field, '') or ''
                if value:
                    contact_details[field] = value
                    break
            else:
                contact_details[field] = ''

        if (not keys) or ('address' in keys):
            contact_details['address'] = self._get_address(contactables)

        if 'website' in contact_details:
            contact_details['website'] = get_valid_url(contact_details['website'])

        return contact_details

    def get_parent_address(self):
        contactables = self._get_contactables()
        url = self.context.REQUEST.URL
        # we don't want self.context address if the object is already created
        if '/++add++' not in url and '/@@add' not in url:
            contactables.remove(self.context)

        address = self._get_address(contactables)
        if not address:
            # Very important to return unicode here, RichTextWidget needs it.
            return u''

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

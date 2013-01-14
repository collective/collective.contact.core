import os.path

from Acquisition import aq_base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contact.content.browser import TEMPLATES_DIR
from collective.contact.content.browser.address import get_address


class Contactable(object):
    """A view for an object that has the IContactDetails behavior fields"""

    person = None
    position = None
    organizations = []

    def get_contactables(self):
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

    def update_contact_details(self):
        contact_details = ['email', 'phone', 'cell_phone', 'im_handle']
        for field in contact_details:
            # search the object that carries the field
            for obj in self.get_contactables():
                obj = aq_base(obj)
                value = getattr(obj, field, '') or ''
                if value:
                    setattr(self, field, value)
                    break
            else:
                setattr(self, field, '')

    def get_address(self):
        # search the object that carries the address
        for obj in self.get_contactables():
            obj = aq_base(obj)
            city = getattr(obj, 'city', '') or ''
            street = getattr(obj, 'street', '') or ''
            if city and street:
                return get_address(obj)
        return {}

    def render_address(self):
        template_path = os.path.join(TEMPLATES_DIR, 'address.pt')
        template = ViewPageTemplateFile(template_path)
        return template(self, self.address)

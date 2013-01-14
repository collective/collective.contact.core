import os.path

from Acquisition import aq_base
from five import grok

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from DateTime import DateTime

from collective.contact.content.held_position import IHeldPosition
from collective.contact.content.browser.address import get_address
from collective.contact.content.browser import TEMPLATES_DIR


grok.templatedir(TEMPLATES_DIR)


def date_to_DateTime(date):
    """Convert datetime.date to DateTime.DateTime format"""
    return DateTime(date.year, date.month, date.day).Date()


class Contact(grok.View):
    grok.name('contact')
    grok.context(IHeldPosition)
    grok.require("zope2.View")
    grok.template('contact')

    def get_contactables(self):
        """Build a list of objects which have the IContactDetails behavior
        for each contact information (email, phone, ...)
        we use the one of the first object in this list which have this information
        """
        contactables = []
        contactables.append(self.person)
        contactables.append(self.position)
        contactables.extend(reversed(self.organizations))
        return contactables

    def update(self):
        held_position = self.context

        start_date = held_position.start_date
        if start_date is not None:
            start_date = date_to_DateTime(start_date)
            self.start_date = self.context.toLocalizedTime(start_date)

        end_date = held_position.end_date
        if end_date is not None:
            end_date = date_to_DateTime(end_date)
            self.end_date = self.context.toLocalizedTime(end_date)

        person = held_position.get_person()
        self.person = person
        self.fullname = person.Title()
        birthday = person.birthday
        if birthday is not None:
            birthday = date_to_DateTime(birthday)
            self.birthday = self.context.toLocalizedTime(birthday)

        self.gender = person.gender or ''
        #self.photo = person.photo or ''  # FIXME:

        position = held_position.get_position()
        self.position = position
        if position is not None:
            self.position_name = position.Title()
        else:
            self.position_name = ''

        organization = held_position.get_organization()
        self.organizations = organization.get_organizations_chain()
        self.organizations_names = organization.get_organizations_titles()

        contactables = self.get_contactables()

        contact_details = ['email', 'phone', 'cell_phone', 'im_handle']
        for field in contact_details:
            # search the object that carries the field
            for obj in contactables:
                obj = aq_base(obj)
                value = getattr(obj, field, '') or ''
                if value:
                    setattr(self, field, value)
                    break
            else:
                setattr(self, field, '')

        # search the object that carries the address
        self.address = None
        for obj in contactables:
            obj = aq_base(obj)
            city = getattr(obj, 'city', '') or ''
            street = getattr(obj, 'street', '') or ''
            if city and street:
                self.address = get_address(obj)
                break

    def render_address(self):
        template_path = os.path.join(TEMPLATES_DIR, 'address.pt')
        template = ViewPageTemplateFile(template_path)
        return template(self, self.address)

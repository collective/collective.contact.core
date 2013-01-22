from plone.dexterity.browser.view import DefaultView

from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.browser.utils import get_ttw_fields,\
    date_to_DateTime


class Contact(DefaultView, Contactable):

    start_date = ''
    end_date = ''
    birthday = ''
    gender = ''
    photo = ''
    position = None
    organizations = []

    def update(self):
        super(Contact, self).update()
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
        #self.photo = person.photo or ''  # FIXME

        self.position = held_position.get_position()

        organization = held_position.get_organization()
        self.organizations = organization.get_organizations_chain()

        self.contactables = self.get_contactables()
        self.update_contact_details()
        self.address = self.get_address()

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(held_position)

from Products.CMFCore.utils import getToolByName

from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.browser.utils import date_to_DateTime,\
                                                     get_ttw_fields
from collective.contact.core.interfaces import IContactable
from collective.contact.core.behaviors import IBirthday


class Person(BaseView):

    name = ''
    birthday = ''
    person_title = ''
    gender = ''
    held_positions = ''
    photo = ''

    def update(self):
        super(Person, self).update()
        self.person = self.context
        person = self.person

        self.name = person.Title()
        if IBirthday.providedBy(person):
            birthday = person.birthday
            if birthday is not None:
                birthday = date_to_DateTime(birthday)
                self.birthday = self.context.toLocalizedTime(birthday)
        else:
            self.birthday = ""

        self.person_title = person.person_title
        self.gender = person.gender or ''

        catalog = getToolByName(self.context, 'portal_catalog')
        context_path = '/'.join(person.getPhysicalPath())
        results = catalog.searchResults(path={'query': context_path,
                                              'depth': 1})
        self.held_positions = results

        contactable = IContactable(person)
        contact_details = contactable.get_contact_details()
        self.email = contact_details['email']
        self.phone = contact_details['phone']
        self.cell_phone = contact_details['cell_phone']
        self.im_handle = contact_details['im_handle']
        self.address = contact_details['address']

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(person)

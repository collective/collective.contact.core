from Products.CMFCore.utils import getToolByName

from plone.dexterity.browser.view import DefaultView

from collective.contact.content.browser.contactable import Contactable

from collective.contact.content.browser.utils import date_to_DateTime,\
    get_ttw_fields


class Person(DefaultView, Contactable):

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
        birthday = person.birthday
        if birthday is not None:
            birthday = date_to_DateTime(birthday)
            self.birthday = self.context.toLocalizedTime(birthday)

        self.person_title = person.person_title
        self.gender = person.gender or ''
        #self.photo = person.photo  # TODO:

        catalog = getToolByName(self.context, 'portal_catalog')
        context_path = '/'.join(person.getPhysicalPath())
        results = catalog.searchResults(path={'query': context_path,
                                              'depth': 1})
        self.held_positions = results

        self.contactables = self.get_contactables()
        self.update_contact_details()
        self.address = self.get_address()

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(person)

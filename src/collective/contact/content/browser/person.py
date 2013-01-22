from five import grok

from Products.CMFCore.utils import getToolByName

from collective.contact.content.browser import TEMPLATES_DIR
from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.content.person import IPerson
from collective.contact.content.browser.utils import date_to_DateTime


grok.templatedir(TEMPLATES_DIR)


class Person(grok.View, Contactable):
    grok.name('person')
    grok.context(IPerson)
    grok.require("zope2.View")
    grok.template('person')

    name = ''
    birthday = ''
    person_title = ''
    gender = ''
    held_positions = ''
    photo = ''

    def update(self):
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

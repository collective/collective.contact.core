from five import grok

from Products.CMFCore.utils import getToolByName

from collective.contact.core.behaviors import IBirthday
from collective.contact.core.browser import TEMPLATES_DIR
from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.browser.utils import date_to_DateTime,\
                                                  get_ttw_fields
from collective.contact.core.content.person import IPerson
from collective.contact.core.interfaces import IContactable


grok.templatedir(TEMPLATES_DIR)


class Person(BaseView):

    name = ''
    birthday = ''
    person_title = ''
    gender = ''
    held_positions = ''

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

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(person)


class HeldPositions(grok.View):
    """Displays held positions list"""
    grok.name('heldpositions')
    grok.template('heldpositions')
    grok.context(IPerson)

    def update(self):
        person = self.context
        catalog = getToolByName(person, 'portal_catalog')
        context_path = '/'.join(person.getPhysicalPath())
        self.held_positions = catalog.searchResults(path={'query': context_path, 'depth': 1})

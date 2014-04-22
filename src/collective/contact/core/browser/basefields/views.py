from AccessControl import getSecurityManager

from five import grok

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.contact.core.behaviors import IBirthday
from collective.contact.core.browser.utils import date_to_DateTime
from collective.contact.core.content.person import IPerson
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.content.position import IPosition
from collective.contact.core.content.held_position import IHeldPosition


grok.templatedir('templates')


class PersonBaseFields(grok.View):
    grok.name('basefields')
    grok.template('person')
    grok.context(IPerson)

    name = ''
    birthday = ''
    person_title = ''
    gender = ''

    def update(self):
        self.person = self.context
        person = self.person
        sm = getSecurityManager()

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
        self.can_edit = sm.checkPermission('Modify portal content', person)


class OrganizationBaseFields(grok.View):

    grok.name('basefields')
    grok.template('organization')
    grok.context(IOrganization)

    name = ''
    type = ''
    positions = []
    activity = ''

    def update(self):
        self.organization = self.context
        organization = self.organization

        self.name = organization.Title()
        factory = getUtility(IVocabularyFactory, "OrganizationTypesOrLevels")
        vocabulary = factory(self.context)
        try:
            self.type = vocabulary.getTerm(organization.organization_type).title
        except LookupError:
            pass
        self.activity = self.context.activity


class PositionBaseFields(grok.View):

    grok.name('basefields')
    grok.template('position')
    grok.context(IPosition)

    name = ''
    type = ''

    def update(self):
        self.position = self.context
        position = self.position
        self.name = position.get_full_title()
        factory = getUtility(IVocabularyFactory, "PositionTypes")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(position.position_type).title


class HeldPositionBaseFields(grok.View):
    grok.name('basefields')
    grok.template('held_position')
    grok.context(IHeldPosition)

    start_date = ''
    end_date = ''
    birthday = ''
    gender = ''
    position = None
    organizations = []

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
        self.title = held_position.Title()

        self.position = held_position.get_position()

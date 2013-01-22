from five import grok
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.contact.content.browser import TEMPLATES_DIR
from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.content.position import IPosition


grok.templatedir(TEMPLATES_DIR)


class Position(grok.View, Contactable):
    grok.name('position')
    grok.context(IPosition)
    grok.require("zope2.View")
    grok.template('position')

    name = ''
    type = ''
    organizations = []

    def update(self):
        self.position = self.context
        position = self.position
        self.name = position.Title()
        factory = getUtility(IVocabularyFactory, "PositionTypes")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(position.position_type).title

        organization = position.get_organization()
        self.organizations = organization.get_organizations_chain()

        self.contactables = self.get_contactables()
        self.update_contact_details()
        self.address = self.get_address()

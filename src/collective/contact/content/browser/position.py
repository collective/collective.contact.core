from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from plone.dexterity.browser.view import DefaultView

from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.browser.utils import get_ttw_fields


class Position(DefaultView, Contactable):

    name = ''
    type = ''
    organizations = []

    def update(self):
        super(Position, self).update()
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

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(position)

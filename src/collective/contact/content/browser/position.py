from five import grok

from collective.contact.content.browser import TEMPLATES_DIR
from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.position import IPosition


grok.templatedir(TEMPLATES_DIR)


class Position(grok.View, Contactable):
    grok.name('position')
    grok.context(IPosition)
    grok.require("zope2.View")
    grok.template('position')

    def update(self):
        self.position = self.context
        position = self.position
        self.name = position.Title()
        self.type = position.position_type  # TODO: get value, not token

        organization = position.get_organization()
        self.organizations = organization.get_organizations_chain()

        self.contactables = self.get_contactables()
        self.update_contact_details()
        self.address = self.get_address()

from five import grok
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from collective.contact.content.browser import TEMPLATES_DIR
from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.content.organization import IOrganization


grok.templatedir(TEMPLATES_DIR)


class Organization(grok.View, Contactable):
    grok.name('organization')
    grok.context(IOrganization)
    grok.require("zope2.View")
    grok.template('organization')

    def update(self):
        self.organization = self.context
        organization = self.organization

        self.name = organization.Title()
        factory = getUtility(IVocabularyFactory, "OrganizationTypesOrLevels")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(organization.organization_type).title

        organizations = organization.get_organizations_chain()
        self.parent_organizations = [org for org in organizations]
        self.parent_organizations.remove(organization)
        self.organizations = organizations

        catalog = getToolByName(self.context, 'portal_catalog')
        context_path = '/'.join(organization.getPhysicalPath())
        self.sub_organizations = catalog.searchResults(portal_type="organization",
                                                       path={'query': context_path,
                                                             'depth': 1})
        self.positions = catalog.searchResults(portal_type="position",
                                               path={'query': context_path,
                                                     'depth': 1})

        self.contactables = self.get_contactables()
        self.update_contact_details()
        self.address = self.get_address()

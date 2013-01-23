from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from plone.dexterity.browser.view import DefaultView

from collective.contact.content.browser.contactable import Contactable
from collective.contact.content.browser.utils import get_ttw_fields


class Organization(Contactable, DefaultView):

    name = ''
    type = ''
    parent_organizations = []
    sub_organizations = []
    positions = []

    def update(self):
        super(Organization, self).update()
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

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(organization)

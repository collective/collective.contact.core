from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from collective.contact.content.browser.contactable import BaseView
from collective.contact.content.browser.utils import get_ttw_fields
from collective.contact.content.interfaces import IContactable


class Organization(BaseView):

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

        contactable = IContactable(organization)
        organizations = contactable.organizations
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

        contact_details = contactable.get_contact_details()
        self.email = contact_details['email']
        self.phone = contact_details['phone']
        self.cell_phone = contact_details['cell_phone']
        self.im_handle = contact_details['im_handle']
        self.address = contact_details['address']

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(organization)

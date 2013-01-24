from Acquisition import aq_inner, aq_chain
from zope.interface import implements
from zope import schema
from z3c.form.interfaces import NO_VALUE

from five import grok

from Products.CMFPlone.utils import base_hasattr

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.content import _
from collective.contact.content.interfaces import IContactContent
from collective.contact.content.browser.contactable import Contactable


class IOrganization(model.Schema, IContactContent):
    """ """

    organization_type = schema.Choice(
        title=_("Type or level"),
        vocabulary="OrganizationTypesOrLevels",
        )

    def get_organizations_chain():
        """Gets chain of organizations
        e.g. for HR service in Division Bar in Organization Foo :
        [OrganizationFoo, DivisionBar, HRService]
        """

    def get_organizations_titles():
        """Gets list of titles of the chain of organizations
        e.g. for HR service in Division Bar in Organization Foo :
        ["Organization Foo", "Division Bar", "HR service"]
        """

    def get_full_title():
        """Gets formated title using list of titles of the organizations
        e.g. for HR service in Division Bar in Organization Foo :
        "Organization Foo / Division Bar / HR service"
        """


class OrganizationContactableAdapter(Contactable):
    grok.context(IOrganization)

    @property
    def organizations(self):
        return self.context.get_organizations_chain()


class Organization(Container):
    """ """
    implements(IOrganization)
    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def get_organizations_chain(self):
        organizations_chain = []
        for item in aq_chain(aq_inner(self)):
            if base_hasattr(item, 'portal_type'):
                if item.portal_type == 'directory':
                    break
                elif item.portal_type == 'organization':
                    organizations_chain.append(item)
        organizations_chain.reverse()
        return organizations_chain

    def get_root_organization(self):
        return self.get_organizations_chain()[0]

    def get_organizations_titles(self):
        return [item.Title() for item in self.get_organizations_chain()]

    def get_full_title(self):
        return ' / '.join(self.get_organizations_titles())


class OrganizationSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_organization")

    def bases(self, schemaName, tree):
        return (IOrganization,)

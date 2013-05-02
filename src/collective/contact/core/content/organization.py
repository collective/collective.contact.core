from Acquisition import aq_inner, aq_chain
from zope.interface import implements
from zope import schema
from z3c.form.interfaces import NO_VALUE

from five import grok

from Products.CMFPlone.utils import base_hasattr

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.core import _
from collective.contact.core.browser.contactable import Contactable
from collective.contact.widget.interfaces import IContactContent


class IOrganization(model.Schema, IContactContent):
    """Interface for Organization content type"""

    organization_type = schema.Choice(
        title=_("Type or level"),
        vocabulary="OrganizationTypesOrLevels",
        )

    def get_organizations_chain():
        """Returns the list of organizations and sub-organizations in this organization
        e.g. for HR service in Division Bar in Organization Foo :
        [OrganizationFoo, DivisionBar, HRService]
        """

    def get_root_organization(self):
        """Returns the first organization in the chain
        e.g. the company or the institution
        """

    def get_organizations_titles(self):
        """Returns the list of titles of the organizations and
        sub-organizations in this organization
        e.g. for HR service in Division Bar in Organization Foo :
        ["Organization Foo", "Division Bar", "HR service"]
        """

    def get_full_title(self):
        """Returns the full title of the organization
        It is constituted by the list of the names of the organizations and
        sub-organizations in this organization separated by slashes
        e.g. for HR service in Division Bar in Organization Foo :
        u"Organization Foo / Division Bar / HR service"
        """


class OrganizationContactableAdapter(Contactable):
    """Contactable adapter for Organization content type"""

    grok.context(IOrganization)

    @property
    def organizations(self):
        return self.context.get_organizations_chain()


class Organization(Container):
    """Organization content type"""
    implements(IOrganization)

    meta_type = 'organization'
    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def get_organizations_chain(self):
        """Returns the list of organizations and sub-organizations in this organization
        e.g. for HR service in Division Bar in Organization Foo :
        [OrganizationFoo, DivisionBar, HRService]
        """
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
        """Returns the first organization in the chain
        e.g. the company or the institution
        """
        return self.get_organizations_chain()[0]

    def get_organizations_titles(self):
        """Returns the list of titles of the organizations and
        sub-organizations in this organization
        e.g. for HR service in Division Bar in Organization Foo :
        [u"Organization Foo", u"Division Bar", u"HR service"]
        """
        return [item.title for item in self.get_organizations_chain()]

    def get_full_title(self):
        """Returns the full title of the organization
        It is constituted by the list of the names of the organizations and
        sub-organizations in this organization separated by slashes
        e.g. for HR service in Division Bar in Organization Foo :
        u"Organization Foo / Division Bar / HR service"
        """
        return u' / '.join(self.get_organizations_titles())


class OrganizationSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """Schema policy for Organization content type"""

    grok.name("schema_policy_organization")

    def bases(self, schemaName, tree):
        return (IOrganization,)

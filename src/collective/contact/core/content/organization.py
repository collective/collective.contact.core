from Acquisition import aq_inner, aq_chain
from zope.interface import implements
from zope import schema
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from zc.relation.interfaces import ICatalog

from five import grok

from Products.CMFPlone.utils import base_hasattr
from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.namedfile.field import NamedImage
from plone.app.textfield import RichText

from collective.contact.core import _
from collective.contact.core.browser.contactable import Contactable
from collective.contact.widget.interfaces import IContactContent
from collective.contact.core.content.held_position import IHeldPosition


class IOrganization(model.Schema, IContactContent):
    """Interface for Organization content type"""

    activity = RichText(
        title=_("Activity"),
        required=False,
        )

    organization_type = schema.Choice(
        title=_("Type or level"),
        vocabulary="OrganizationTypesOrLevels",
    )

    logo = NamedImage(
        title=_("Logo"),
        required=False,
        )

    def get_organizations_chain(self):
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

    def get_positions(self):
        """Returns the positions"""

    def get_held_positions(self):
        """Returns the held positions
           that have been directly linked to the organization
           without a position
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

    def get_organizations_chain(self, first_index=0):
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
        return organizations_chain[first_index:]

    def get_root_organization(self):
        """Returns the first organization in the chain
        e.g. the company or the institution
        """
        return self.get_organizations_chain()[0]

    def get_organizations_titles(self, first_index=0):
        """Returns the list of titles of the organizations and
        sub-organizations in this organization
        e.g. for HR service in Division Bar in Organization Foo :
        [u"Organization Foo", u"Division Bar", u"HR service"]
        """
        return [item.title for item in self.get_organizations_chain(first_index=first_index)]

    def get_full_title(self, separator=u' / ', first_index=0):
        """Returns the full title of the organization
        It is constituted by the list of the names of the organizations and
        sub-organizations in this organization separated by slashes
        e.g. for HR service in Division Bar in Organization Foo :
        u"Organization Foo / Division Bar / HR service"
        """
        return separator.join(self.get_organizations_titles(first_index=first_index))

    def get_positions(self):
        catalog = api.portal.get_tool('portal_catalog')
        positions = catalog.searchResults(portal_type="position",
                                          path={'query': '/'.join(self.getPhysicalPath()),
                                                'depth': 1})
        return [c.getObject() for c in positions]

    def get_held_positions(self):
        """Returns the held positions
           that have been directly linked to the organization
           without a position
        """
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        orga_intid = intids.getId(self)
        contact_relations = catalog.findRelations(
                              {'to_id': orga_intid,
                               'from_interfaces_flattened': IHeldPosition,
                               'from_attribute': 'position'})
        return [c.from_object for c in contact_relations]


class OrganizationSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """Schema policy for Organization content type"""

    grok.name("schema_policy_organization")

    def bases(self, schemaName, tree):
        return (IOrganization,)

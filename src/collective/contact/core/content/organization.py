from Acquisition import aq_chain
from Acquisition import aq_inner
from collective.contact.core import _
from collective.contact.core import logger
from collective.contact.core.browser.contactable import Contactable
from collective.contact.core.interfaces import IHeldPosition
from collective.contact.widget.interfaces import IContactContent
from five import grok
from plone import api
from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.namedfile.field import NamedImage
from plone.supermodel import model
from Products.CMFPlone.utils import base_hasattr
from zc.relation.interfaces import ICatalog
from zope import schema
from zope.component import getUtility
from zope.interface import implements
from zope.intid.interfaces import IIntIds


class InvalidEnterpriseNumber(schema.ValidationError):
    """Exception for invalid enterprise number"""
    __doc__ = _(u"Enterprise number must contain only letters and numbers")


def validateEnterpriseNumber(value):
    """Enterprise number validator"""
    if not value.isalnum():
        raise InvalidEnterpriseNumber(value)
    return True


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

    enterprise_number = schema.TextLine(
        title=_(u"Enterprise (or VAT) number"),
        required=False,
        constraint=validateEnterpriseNumber,
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
                                                'depth': 1},
                                          sort_on='getObjPositionInParent')
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
        held_positions = []
        for relation in contact_relations:
            held_position = relation.from_object
            if not held_position:
                logger.error(
                    "from_object missing for relation from held_position to organisation %s: %s",
                    self, relation.__dict__)
                continue
            held_positions.append(held_position)
        return held_positions


class OrganizationSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """Schema policy for Organization content type"""

    grok.name("schema_policy_organization")

    def bases(self, schemaName, tree):
        return (IOrganization,)

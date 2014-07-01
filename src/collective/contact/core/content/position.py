from zope.interface import implements
from zope import schema
from z3c.form.interfaces import NO_VALUE

from five import grok

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.core import _
from collective.contact.core.browser.contactable import Contactable
from collective.contact.widget.interfaces import IContactContent
from zope.component._api import getUtility
from zope.intid.interfaces import IIntIds
from zc.relation.interfaces import ICatalog
from collective.contact.core.content.held_position import IHeldPosition


class IPosition(model.Schema, IContactContent):
    """Interface for Position content type"""

    position_type = schema.Choice(
        title=_("Type"),
        vocabulary="PositionTypes",
        )

    def get_organization(self):
        """Returns the organization to which the position is linked"""

    def get_full_title(self):
        """Returns the full title of the position
        It is constituted by the name of the position and
        the name of its organization in brackets
        """


class PositionContactableAdapter(Contactable):
    """Contactable adapter for Position content type"""

    grok.context(IPosition)

    @property
    def position(self):
        return self.context

    @property
    def organizations(self):
        organization = self.context.get_organization()
        return organization.get_organizations_chain()


class Position(Container):
    """Position content type"""

    implements(IPosition)

    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def get_organization(self):
        """Returns the organization to which the position is linked"""
        return self.getParentNode()

    def get_organizations_chain(self, first_index=0):
        """Return all organizations in the chain AND the position itself
        """
        organization = self.get_organization()
        chain = organization.get_organizations_chain(first_index=first_index)
        chain.append(self)
        return chain

    def get_full_title(self):
        """Returns the full title of the position
        It is constituted by the name of the position,
        the name of its organization and the name of the
        root organization in brackets.
        """
        organization = self.get_organization()
        root_organization = organization.get_root_organization()
        if organization == root_organization:
            return u"%s (%s)" % (self.title, organization.title)
        else:
            return u"%s, %s (%s)" % (self.title, organization.title,
                                     root_organization.title)

    def get_held_positions(self):
        """Returns the held position
           that have been linked to this position
        """
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        position_intid = intids.getId(self)
        contact_relations = catalog.findRelations(
                              {'to_id': position_intid,
                               'from_interfaces_flattened': IHeldPosition,
                               'from_attribute': 'position'})
        return [c.from_object for c in contact_relations]


class PositionSchemaPolicy(grok.GlobalUtility,
                           DexteritySchemaPolicy):
    """Schema policy for Position content type"""

    grok.name("schema_policy_position")

    def bases(self, schemaName, tree):
        return (IPosition,)

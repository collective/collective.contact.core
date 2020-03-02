# -*- coding: utf-8 -*-
from collective.contact.core import _
from collective.contact.core import logger
from collective.contact.core.browser.contactable import Contactable
from collective.contact.widget.interfaces import IContactContent
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model
from z3c.form.interfaces import NO_VALUE
from zc.relation.interfaces import ICatalog
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds


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

    @property
    def position(self):
        return self.context

    @property
    def organizations(self):
        organization = self.context.get_organization()
        return organization.get_organizations_chain()


@implementer(IPosition)
class Position(Container):
    """Position content type"""

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

    def get_full_title(self, separator=u' / ', first_index=0):
        """Returns the full title of the position
        It is constituted by the name of the position,
        the full name of its organization.
        """
        organization = self.get_organization()
        return u"%s (%s)" % (self.title, organization.get_full_title(separator=separator, first_index=first_index))

    def get_held_positions(self):
        """Returns the held position
           that have been linked to this position
        """
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        position_intid = intids.getId(self)
        contact_relations = catalog.findRelations(
            {'to_id': position_intid,
             'from_attribute': 'position'}
        )
        held_positions = []
        for relation in contact_relations:
            held_position = relation.from_object
            if not held_position:
                logger.error("from_object missing for relation from held_position to position %s: %s", self,
                             relation.__dict__)
                continue
            held_positions.append(held_position)
        return held_positions


class PositionSchemaPolicy(DexteritySchemaPolicy):
    """Schema policy for Position content type"""

    def bases(self, schemaName, tree):
        return (IPosition,)

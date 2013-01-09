from zope.interface import implements
from zope import schema
from z3c.relationfield.schema import RelationChoice

from five import grok

from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container
from plone.supermodel import model

from . import _


class IHeldPosition(model.Schema):

    # TODO: title of Position + start_date + end_date

    start_date = schema.Date(
      title=_("Start date"),
    )
    end_date = schema.Date(
      title=_("End date")
    )
    position = RelationChoice(
        title=_("Position or organization"),
        source=ObjPathSourceBinder(portal_type=("organization", "position"))
    )

    def get_person():
        """Get the person who helds the position
        """


class HeldPosition(Container):
    """Position held by a person in an organization"""
    implements(IHeldPosition)

    def get_person(self):
        return self.getParentNode()


class HeldPositionSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_held_position")

    def bases(self, schemaName, tree):
        return (IHeldPosition,)

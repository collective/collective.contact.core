from zope.interface import implements
from zope import schema

from five import grok

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from . import _


class IPosition(model.Schema):
    """ """

    position_type = schema.Choice(
        title=_("Type"),
        vocabulary="PositionTypes",
        )

    def get_organization():
        """Returns organization"""


class Position(Container):
    """ """
    implements(IPosition)

    def get_organization(self):
        return self.getParentNode()


class PositionSchemaPolicy(grok.GlobalUtility,
                           DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_position")

    def bases(self, schemaName, tree):
        return (IPosition,)

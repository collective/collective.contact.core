from zope.interface import implements
from zope import schema

from five import grok

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.contact.content import _
from collective.contact.content.interfaces import IContactContent
from collective.contact.content.browser.contactable import Contactable


class IPosition(model.Schema, IContactContent):
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

    def get_full_title(self):
        organization = self.get_organization().Title()
        return "%s (%s)" % (self.Title(), organization)


class PositionSchemaPolicy(grok.GlobalUtility,
                           DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_position")

    def bases(self, schemaName, tree):
        return (IPosition,)

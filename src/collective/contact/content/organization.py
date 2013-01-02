from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.directives.form import default_value
from plone.dexterity.schema import DexteritySchemaPolicy

from . import _


class IOrganization(model.Schema):
    """ """

    organization_type = schema.Choice(
        title=_("Type or level"),
        vocabulary="OrganizationTypesOrLevels",
        )


class Organization(Container):
    """ """
    implements(IOrganization)


class OrganizationSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IOrganization,)

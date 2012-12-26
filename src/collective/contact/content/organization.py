from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.directives.form import default_value
from plone.dexterity.schema import DexteritySchemaPolicy

from . import _




class IOrganization(model.Schema):
    """ """

    is_root_organization = schema.Bool(
        title=_("Is root ?"),
        # TODO: hide this field !
        )

    organization_type = schema.Choice(
        title=_("Type or level"),
        vocabulary="OrganizationTypesOrLevels",
        )

@default_value(field=IOrganization['is_root_organisation'])
def isRootOrganization(data):
    if data.context.getPortalTypeName() == 'directory':
        return True
    #elif data.context.getPortalTypeName() == 'organization':
    else:
        return False


class Organization(Container):
    """ """
    implements(IOrganization)


class OrganizationSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IOrganization,)


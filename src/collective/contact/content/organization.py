from zope.interface import implements
from zope import schema

from Acquisition import aq_inner, aq_chain

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.dexterity.schema import DexteritySchemaPolicy

from . import _
from Products.CMFPlone.utils import base_hasattr


class IOrganization(model.Schema):
    """ """

    organization_type = schema.Choice(
        title=_("Type or level"),
        vocabulary="OrganizationTypesOrLevels",
        )


class Organization(Container):
    """ """
    implements(IOrganization)

    def get_full_title(self):
        full_title = []
        for item in aq_chain(aq_inner(self)):
            if base_hasattr(item, 'portal_type'):
                if item.portal_type == 'directory':
                    break
                elif item.portal_type == 'organization':
                    full_title.append(item.Title())
        return reversed(full_title)


class OrganizationSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IOrganization,)

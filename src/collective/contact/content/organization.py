from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.parser import ISchemaPolicy

from . import _


class IOrganization(model.Schema):

    organization_type = schema.Choice(
      title=_("Type"),
      vocabulary="OrganizationTypes"
      )


class Organization(Container):
    """ """
    implements(IOrganization)


class OrganizationSchemaPolicy(object):
    """ """
    implements(ISchemaPolicy)
    
    def module(self, schemaName, tree):
        return 'plone.dexterity.schema.transient'
        
    def bases(self, schemaName, tree):
        return (IOrganization,)
        
    def name(self, schemaName, tree):
        # We use a temporary name whilst the interface is being generated;
        # when it's first used, we know the portal_type and site, and can
        # thus update it
        return '__tmp__' + schemaName


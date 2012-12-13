from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model

from . import _


class IOrganization(model.Schema):

    organization_type = schema.Choice(
      title=_("Type"),
      vocabulary="OrganizationTypes"
      )


class Organization(Container):
    """ """
    implements(IOrganization)

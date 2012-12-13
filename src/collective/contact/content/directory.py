from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.supermodel import model

from . import _


class IDirectory(model.Schema):
    
    position_types = schema.Text(
        title=_("Position types"),
        )
    organization_types = schema.Text(
        title=_("Organization types"),
        )
    organization_levels=schema.Text(
        title=_("Organization levels"),
        )
  
class Directory(Container):
    """ """
    implements(IDirectory)

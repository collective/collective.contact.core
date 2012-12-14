from zope.interface import implements
from zope import schema
from plone.namedfile.field import NamedImage

from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.parser import ISchemaPolicy

from . import _


class IPerson(model.Schema):

    lastname = schema.TextLine(
        title=_(u"Lastname"),
        required=True
        )
    gender = schema.Choice(
       required=False,
       values=("M", "F",),
        )
    person_title = schema.TextLine(
        required=False,
        title=_("Person title"),
        )
    firstname = schema.TextLine(
        required=False,
        title=_("Firstname"),
        )
    lastname = schema.TextLine(
        title=_("Lastname")
        )
    birthday = schema.Date(
        required=False,
        title=_("Birthday"),
        )
    email = schema.TextLine(
      required=False,
      title=_("Email"),
        )
    photo = NamedImage(
      required=False,
      title=_("Photo"),
        )


class Person(Container):
    """ """
    implements(IPerson)


class PersonSchemaPolicy(object):
    """ """
    implements(ISchemaPolicy)
    
    def module(self, schemaName, tree):
        return 'plone.dexterity.schema.transient'
        
    def bases(self, schemaName, tree):
        return (IPerson, )
        
    def name(self, schemaName, tree):
        # We use a temporary name whilst the interface is being generated;
        # when it's first used, we know the portal_type and site, and can
        # thus update it
        return '__tmp__' + schemaName


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

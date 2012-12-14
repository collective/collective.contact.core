from zope import schema
from zope.interface import implements

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.namedfile.field import NamedImage
from plone.supermodel import model

from . import _


class IPerson(model.Schema):
    """ """

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


class PersonSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IPerson, )


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
        title=_("Gender"),
        values=("M", "F",),
        required=False,
        )
    person_title = schema.TextLine(
        title=_("Person title"),
        required=False,
        )
    firstname = schema.TextLine(
        title=_("Firstname"),
        required=False,
        )
    lastname = schema.TextLine(
        title=_("Lastname")
        )
    birthday = schema.Date(
        title=_("Birthday"),
        required=False,
        )
    photo = NamedImage(
        title=_("Photo"),
        required=False,
        )


class Person(Container):
    """ """
    implements(IPerson)

    def Title(self):
        person_title = self.person_title or ''
        firstname = self.firstname or ''
        lastname = self.lastname or ''
        return ' '.join((person_title, firstname, lastname))


class PersonSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IPerson, )

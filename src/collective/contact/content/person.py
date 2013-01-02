from zope import schema
from zope.component import adapts
from zope.interface import implements

from plone.app.content.interfaces import INameFromTitle

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from plone.namedfile.field import NamedImage
from plone.supermodel import model

from . import _


class INameFromPersonNames(INameFromTitle):

    def title(self):
        """Return a processed title"""


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
    email = schema.TextLine(
        title=_("Email"),
        required=False,
        )
    photo = NamedImage(
        title=_("Photo"),
        required=False,
        )


class NameFromPersonNames(object):
    adapts(IPerson)
    implements(INameFromPersonNames)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        firstname = self.context.firstname
        lastname = self.context.lastname
        if firstname is not None and firstname:
            return firstname + ' ' + lastname
        else:
            return lastname


class Person(Container):
    """ """
    implements(IPerson)


class PersonSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IPerson, )

from zope import schema
from zope.interface import implements

from five import grok

from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.namedfile.field import NamedImage
from plone.supermodel import model

from collective.contact.content import _


class IPerson(model.Schema):
    """ """

    lastname = schema.TextLine(
        title=_("Lastname"),
        required=True
        )
    firstname = schema.TextLine(
        title=_("Firstname"),
        required=False,
        )
    gender = schema.Choice(
        title=_("Gender"),
        vocabulary="Genders",
        required=False,
        )
    person_title = schema.TextLine(
        title=_("Person title"),
        required=False,
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
        # must return utf8 and not unicode (Title() from basic behavior return utf8)
        # attributes are stored as unicode
        person_title = self.person_title or ''
        firstname = self.firstname or ''
        lastname = self.lastname or ''
        return ' '.join([e.encode('utf8') for e in (person_title, firstname, lastname) if e])


class PersonSchemaPolicy(grok.GlobalUtility,
                         DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_person")

    def bases(self, schemaName, tree):
        return (IPerson, )

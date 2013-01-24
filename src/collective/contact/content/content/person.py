from zope import schema
from zope.interface import implements
from z3c.form.interfaces import NO_VALUE
from z3c.form.browser.radio import RadioFieldWidget

from five import grok

from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.namedfile.field import NamedImage
from plone.supermodel import model

from collective.contact.content import _
from collective.contact.content.interfaces import IContactContent
from collective.contact.content.browser.contactable import Contactable


class IPerson(model.Schema, IContactContent):
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
    form.widget(gender=RadioFieldWidget)
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


class PersonContactableAdapter(Contactable):
    grok.context(IPerson)

    @property
    def person(self):
        return self.context


class Person(Container):
    """ """
    implements(IPerson)
    # plone.dexterity.content.Content.__getattr__ retrieve the field.default
    # so step 1.2.1 in z3c.form.widget.py returns something instead of NO_VALUE
    # then IValue adapter is not looked up...
    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

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

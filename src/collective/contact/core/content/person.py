from zope import schema
from zope.interface import implements
from zope.interface import Attribute
from z3c.form.interfaces import NO_VALUE
from z3c.form.browser.radio import RadioFieldWidget

from five import grok

from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.namedfile.field import NamedImage
from plone.supermodel import model

from collective.contact.core import _
from collective.contact.core.browser.contactable import Contactable
from collective.contact.widget.interfaces import IContactContent
from collective.contact.core.content.held_position import IHeldPosition


class IPerson(model.Schema, IContactContent):
    """Interface for Person content type"""

    is_created = Attribute(u"Marker to know if the object is already created")

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

    def get_held_positions(self):
        """Returns held positions of this person
        """

class PersonContactableAdapter(Contactable):
    """Contactable adapter for Person content type"""

    grok.context(IPerson)

    @property
    def person(self):
        return self.context


class Person(Container):
    """Person content type"""

    implements(IPerson)

    meta_type = 'person'
    is_created = False
    # plone.dexterity.content.Content.__getattr__ retrieve the field.default
    # so step 1.2.1 in z3c.form.widget.py returns something instead of NO_VALUE
    # then IValue adapter is not looked up...
    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def get_title(self):
        return u' '.join([x for x in (self.person_title, self.firstname, self.lastname) if x])

    def Title(self):
        # must return utf8 and not unicode (Title() from basic behavior return utf8)
        # attributes are stored as unicode
        return self.get_title().encode('utf-8')

    def get_held_positions(self):
        return [obj for obj in self.values() if IHeldPosition.providedBy(obj)]

class PersonSchemaPolicy(grok.GlobalUtility,
                         DexteritySchemaPolicy):
    """Schema policy for Person content type"""

    grok.name("schema_policy_person")

    def bases(self, schemaName, tree):
        return (IPerson, )

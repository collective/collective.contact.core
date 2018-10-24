# -*- coding: utf-8 -*-

from collective.contact.core import _
from collective.contact.core.browser.contactable import Contactable
from collective.contact.core.interfaces import IContactable
from collective.contact.core.interfaces import IContactCoreParameters
from collective.contact.core.interfaces import IHeldPosition
from collective.contact.core.interfaces import IPersonHeldPositions
from collective.contact.widget.interfaces import IContactContent
from five import grok
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.namedfile.field import NamedImage
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from Products.CMFPlone.utils import normalizeString
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import NO_VALUE
from zope import schema
from zope.cachedescriptors.property import CachedProperty
from zope.component import queryUtility
from zope.interface import implements


class IPerson(model.Schema, IContactContent):
    """Interface for Person content type"""

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
        description=_('help_person_title',
                      u"Doctor, Mrs..."),
        required=False,
        )
    photo = NamedImage(
        title=_("Photo"),
        required=False,
        )
    signature = NamedImage(
        title=_("Signature"),
        description=_("Scanned signature"),
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

    @CachedProperty
    def held_position(self):
        return IPersonHeldPositions(self.person).get_main_position()

    @property
    def position(self):
        held_position = self.held_position
        if held_position:
            return IContactable(held_position).position

    @property
    def organizations(self):
        held_position = self.held_position
        if held_position:
            return IContactable(held_position).organizations
        else:
            return ()


class Person(Container):
    """Person content type"""

    implements(IPerson)

    # plone.dexterity.content.Content.__getattr__ retrieve the field.default
    # so step 1.2.1 in z3c.form.widget.py returns something instead of NO_VALUE
    # then IValue adapter is not looked up...
    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def set_title(self, val):
        return

    def get_title(self, include_person_title=True):
        displayed_attrs = ('person_title', 'firstname', 'lastname')
        if not include_person_title:
            displayed_attrs = ('firstname', 'lastname')
        else:
            registry = queryUtility(IRegistry)
            if registry is not None:
                record = registry.forInterface(IContactCoreParameters, None)
                if record is not None:
                    if not record.person_title_in_title:
                        displayed_attrs = ('firstname', 'lastname')

        displayed = [getattr(self, attr, None) for attr in displayed_attrs]
        return u' '.join([x for x in displayed if x])

    title = property(get_title, set_title)

    get_full_title = get_title

    def Title(self):
        # must return utf8 and not unicode (Title() from basic behavior return utf8)
        # attributes are stored as unicode
        return self.get_title().encode('utf-8')

    def get_sortable_title(self):
        if self.firstname is None:
            fullname = self.lastname
        else:
            fullname = u"%s %s" % (self.lastname, self.firstname)
        return normalizeString(fullname)

    def get_held_positions(self):
        return [obj for obj in self.values() if IHeldPosition.providedBy(obj)]

    def get_held_positions_titles(self):
        return [p.Title() for p in self.get_held_positions()]

    def get_full_name(self):
        return u' '.join([x for x in (self.firstname, self.lastname) if x])


class PersonSchemaPolicy(grok.GlobalUtility,
                         DexteritySchemaPolicy):
    """Schema policy for Person content type"""

    grok.name("schema_policy_person")

    def bases(self, schemaName, tree):
        return (IPerson, )

from zope.i18nmessageid import MessageFactory

from plone.autoform.form import AutoExtensibleForm
from plone.autoform import directives as form
import z3c.form
from plone.supermodel import model

from collective.contact.content.content.held_position import IHeldPosition
from collective.contact.content.schema import ContactChoice
from collective.contact.content.source import ContactSourceBinder
from collective.contact.content.widgets import ContactAutocompleteFieldWidget

_ = MessageFactory("collective.contact.content")


class IAddContact(model.Schema):
    organization = ContactChoice(
            title=_(u"Organization"),
            required=False,
            source=ContactSourceBinder(portal_type="organization"))
    form.widget(organization=ContactAutocompleteFieldWidget)

    person = ContactChoice(
            title=_(u"Person"),
            required=False,
            source=ContactSourceBinder(portal_type="person"))
    form.widget(person=ContactAutocompleteFieldWidget)

    position = ContactChoice(
            title=_(u"Position"),
            required=False,
            source=ContactSourceBinder(portal_type="position"))
    form.widget(person=ContactAutocompleteFieldWidget)


class AddContact(AutoExtensibleForm, z3c.form.form.AddForm):
    prefix = "addcontact"
    schema = IAddContact
    additionnalSchema = IHeldPosition

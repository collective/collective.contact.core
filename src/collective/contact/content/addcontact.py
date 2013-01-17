from zope.component import getUtility

from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.browser.add import DefaultAddForm
import z3c.form
from plone.supermodel import model

from collective.contact.content.schema import ContactChoice
from collective.contact.content.source import ContactSourceBinder
from collective.contact.content.widgets import ContactAutocompleteFieldWidget

from plone.dexterity.i18n import MessageFactory as DMF

from . import _


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


class AddContact(DefaultAddForm, z3c.form.form.AddForm):
    label = DMF(u"Add ${name}", mapping={'name': _(u"Contact")})
    description = u""
    schema = IAddContact

    @property
    def additionalSchemata(self):
        fti = getUtility(IDexterityFTI, name='held_position')
        schema = fti.lookupSchema()
        # save the schema name to be able to remove a field afterwards
        self._schema_name = schema.__name__
        return (schema,)

    def updateFieldsFromSchemata(self):
        super(AddContact, self).updateFieldsFromSchemata()
        # IHeldPosition and IAddContact have both a field named position
        # remove the one from IHeldPosition
        self.fields = self.fields.omit('position', prefix=self._schema_name)

    def create(self, data):
        # TODO: see parts/omelette/plone/dexterity/browser/add.py
        raise NotImplementedError

    def add(self, object):
        # TODO: see parts/omelette/plone/dexterity/browser/add.py
        raise NotImplementedError

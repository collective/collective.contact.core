from zope.interface import implements
from zope.component import getUtility
from zope.publisher.browser import BrowserView
from zope.contentprovider.interfaces import IContentProvider

from plone.autoform import directives as form
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.browser.add import DefaultAddForm
import z3c.form
from z3c.form.interfaces import IFieldsAndContentProvidersForm
from z3c.form.contentprovider import ContentProviders
from plone.supermodel import model
from plone.dexterity.i18n import MessageFactory as DMF

from collective.contact.content.schema import ContactChoice
from collective.contact.content.source import ContactSourceBinder
from collective.contact.content.widgets import ContactAutocompleteFieldWidget

from . import _


class MasterSelectAddContactProvider(BrowserView):
    implements(IContentProvider)
    def __init__(self, context, request, view):
        super(MasterSelectAddContactProvider, self).__init__(context, request)
        self.__parent__ = view

    def update(self):
        pass

    def render(self):
# On change event, we don't have the new radio box created yet.
# If we fill organization and person, show position and held position fields
        return """<script type="text/javascript">
$(document).ready(function() {
  var position_fields = '#formfield-form-widgets-position,div[id*=held_position]';
  $(position_fields).hide();
  $('#form-widgets-organization-widgets-query').change(function(e){
    var radio = $('input[name="form.widgets.person:list"]');
    if (radio.length > 1) {
      $(position_fields).show('slow');
    }
  });
  $('#form-widgets-person-widgets-query').change(function(e){
    var radio = $('input[name="form.widgets.organization:list"]');
    if (radio.length > 1) {
      $(position_fields).show('slow');
    }
  });
  $('#form-widgets-position-autocomplete .addnew').hover(function(e){
    var form = $(this).closest('form'),
    viewArr = form.serializeArray(),
    view = {};
    for (var i in viewArr) {
      view[viewArr[i].name] = viewArr[i].value;
    }
    var add_position_url = portal_url + '/' + view['form.widgets.organization:list'].split('/').slice(2).join('/') + '/++add++position';
    $('#form-widgets-position-autocomplete .addnew').data('pbo').src = add_position_url;
  });
});
</script>
"""


class RenderContentProvider(BrowserView):
    def __call__(self):
        return self.context.render()


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
    implements(IFieldsAndContentProvidersForm)
    contentProviders = ContentProviders(['organization-ms'])
#    contentProviders['organization-ms'] = MasterSelectAddContactProvider
    contentProviders['organization-ms'].position = 0
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

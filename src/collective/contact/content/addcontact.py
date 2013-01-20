from zope.component import getUtility
from zope.contentprovider.interfaces import IContentProvider
from zope.event import notify
from zope.interface import implements
from zope.publisher.browser import BrowserView

from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.utils import addContentToContainer
from z3c.form.interfaces import IFieldsAndContentProvidersForm, HIDDEN_MODE
from z3c.form.contentprovider import ContentProviders
from z3c.form import form, button
from plone.supermodel import model
from plone.dexterity.i18n import MessageFactory as DMF
from Products.statusmessages.interfaces import IStatusMessage

from collective.contact.content.schema import ContactChoice
from collective.contact.content.source import ContactSourceBinder

from . import _


class MasterSelectAddContactProvider(BrowserView):
    implements(IContentProvider)
    def __init__(self, context, request, view):
        super(MasterSelectAddContactProvider, self).__init__(context, request)
        self.__parent__ = view

    def update(self):
        pass

    def render(self):
# If we fill organization and person, show position and held position fields
        return """<script type="text/javascript">
$(document).ready(function() {
  $('#formfield-form-widgets-Plone_0_held_position-position').hide();
  var position_fields = '#formfield-form-widgets-position,div[id*=held_position]';
  if (!($('input[name="form.widgets.person:list"]').length > 1 &&
        $('input[name="form.widgets.organization:list"]').length > 1)) {
      $(position_fields).hide();
  }
 function serialize_form(form) {
    viewArr = form.serializeArray(),
    view = {};
    for (var i in viewArr) {
      view[viewArr[i].name] = viewArr[i].value;
    }
    return view;
  }
  function update_position_field(form) {
    var view = serialize_form(form);
    var organization_token = view['form.widgets.organization:list'];
    var organization_title = form.find('#form-widgets-organization-input-fields input[value='+organization_token+']').siblings('.label').text();
    $('#formfield-form-widgets-position > .fieldErrorBox').text('Recherchez ou ajoutez une fonction dans "' + organization_title + '".');
    $("#form-widgets-position-widgets-query")
        .setOptions({extraParams: {path: organization_token}}).flushCache();

    var organization_path = '/' + organization_token.split('/').slice(2).join('/');
    var add_position_url = portal_url + organization_path + '/++add++position';
    $('#form-widgets-position-autocomplete .addnew').data('pbo').src = add_position_url;
  }
  $('#form-widgets-organization-input-fields').delegate('input', 'change', function(e){
    var form = $(this).closest('form');
    update_position_field(form);
    if ($('input[name="form.widgets.person:list"]').length > 1 &&
        $('input[name="form.widgets.organization:list"]').length > 1) {
      $(position_fields).show('slow');
      $('#formfield-form-widgets-Plone_0_held_position-position').hide();
    }
  });
  $('#form-widgets-person-input-fields').delegate('input', 'change', function(e){
    if ($('input[name="form.widgets.person:list"]').length > 1 &&
        $('input[name="form.widgets.organization:list"]').length > 1) {
      $(position_fields).show('slow');
      $('#formfield-form-widgets-Plone_0_held_position-position').hide();
    }
  });
  $('#form-widgets-position-widgets-query').setOptions({minChars: 0});
  $('#form-widgets-position-widgets-query').focus(function(e){
    $(this).trigger('click');
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

    person = ContactChoice(
            title=_(u"Person"),
            required=False,
            source=ContactSourceBinder(portal_type="person"))

    position = ContactChoice(
            title=_(u"Position"),
            required=False,
            source=ContactSourceBinder(portal_type="position"))


class AddContact(DefaultAddForm, form.AddForm):
    implements(IFieldsAndContentProvidersForm)
    contentProviders = ContentProviders(['organization-ms'])
#    contentProviders['organization-ms'] = MasterSelectAddContactProvider
    contentProviders['organization-ms'].position = -1
    label = DMF(u"Add ${name}", mapping={'name': _(u"Contact")})
    description = u""
    schema = IAddContact
    portal_type = 'held_position'

    @property
    def additionalSchemata(self):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        schema = fti.lookupSchema()
        # save the schema name to be able to remove a field afterwards
        self._schema_name = schema.__name__
        return (schema,)

    def updateFieldsFromSchemata(self):
        super(AddContact, self).updateFieldsFromSchemata()
        # IHeldPosition and IAddContact have both a field named position
        # hide the one from IHeldPosition
        # TODO: there is no hidden template for autocomplete widget,
        # we hide it in javascript for now.
        self.fields[self._schema_name+'.position'].mode = HIDDEN_MODE

    def updateWidgets(self):
        super(AddContact, self).updateWidgets()
        for widget in self.widgets.values():
            if getattr(widget, 'required', False):
                # This is really a hack to not have required field errors
                # but have the visual required nevertheless.
                # We need to revert this after updateActions
                # because this change impact the held position form
                widget.field.required = False

    def update(self):
        super(AddContact, self).update()
        # revert required field changes
        for widget in self.widgets.values():
            if getattr(widget, 'required', False):
                widget.field.required = True

    @button.buttonAndHandler(_('Add'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(DMF(u"Item created"), "info")

    @button.buttonAndHandler(DMF(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(DMF(u"Add New Item operation cancelled"), "info")
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))

    def createAndAdd(self, data):
        if data['person'] is None and data['organization'] is None:
            return
        elif data['organization'] is not None and data['person'] is None:
            self.request.response.redirect(data['organization'].absolute_url())
            self._finishedAdd = True
            return
        elif data['person'] is not None and data['organization'] is None:
            self.request.response.redirect(data['person'].absolute_url())
            self._finishedAdd = True
            return
        else:
            return super(AddContact, self).createAndAdd(data)

    def create(self, data):
        self._container = data.pop('person')
        position = data.pop('position')
        orga = data.pop('organization')
        if position is None:
            position = orga

        data[self._schema_name+'.position'] = position
        return super(AddContact, self).create(data)

    def add(self, object):
        container = self._container
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        new_object = addContentToContainer(container, object)

        if fti.immediate_view:
            self.immediate_view = "%s/%s/%s" % (container.absolute_url(), new_object.id, fti.immediate_view,)
        else:
            self.immediate_view = "%s/%s" % (container.absolute_url(), new_object.id)

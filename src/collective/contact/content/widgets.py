from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.component import getUtility
from zope.interface import implementer, Interface
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from five import grok
from Products.CMFCore.utils import getToolByName

from plone.dexterity.interfaces import IDexterityFTI
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.formwidget.autocomplete.widget import (
    AutocompleteMultiSelectionWidget,
    AutocompleteSelectionWidget)

from plone.dexterity.i18n import MessageFactory as DMF

from . import _

class PatchLoadInsideOverlay(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHtmlHeadLinks)

    def render(self):
        return """<script type="text/javascript">
$(document).ready(function() {
  $(document).bind('formOverlayLoadSuccess', function(e, req, myform, api, pb, ajax_parent) {
    var o = ajax_parent.closest('.overlay-ajax');
    var pbo = o.data('pbo');
    if (!pbo.selector) {
      var content = ajax_parent.find(common_content_filter).detach();
      ajax_parent.empty().append(content);
      ajax_parent.prepend(ajax_parent.find('.portalMessage').detach());
      ajax_parent.wrapInner('<div />');
    }
  });
  $(document).bind('formOverlayLoadFailure', function(e, req, myform, api, pb, ajax_parent) {
    var o = ajax_parent.closest('.overlay-ajax');
    var pbo = o.data('pbo');
    if (!pbo.selector) {
      var content = ajax_parent.find(common_content_filter).detach();
      ajax_parent.empty().append(content);
      ajax_parent.prepend(ajax_parent.find('.portalMessage').detach());
      ajax_parent.wrapInner('<div />');
    }
  });
  $(document).bind('loadInsideOverlay', function(e, el, responseText, errorText, api) {
    var el = $(el);
    var o = el.closest('.overlay-ajax');
    var pbo = o.data('pbo');
    var overlay_counter = parseInt(pbo.nt.substring(3, pbo.nt.length));
    o.css({zIndex: 9998+overlay_counter});
//    el.html(responseText);
    if (!pbo.selector) {
      var content = el.find(common_content_filter).detach();
      el.empty().append(content);
      el.wrapInner('<div />');
    }
  });
});
</script>
<style type="text/css">
#calroot {
  z-index: 99999;
}
</style>
"""


def find_directory(context):
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog.searchResults(portal_type='directory')
    return results[0].getObject()


class ContactBaseWidget(object):
    display_template = ViewPageTemplateFile('templates/contact_display.pt')
    input_template = ViewPageTemplateFile('templates/contact_input.pt')

    def render(self):
        source = self.bound_source
        criteria = source.selectable_filter.criteria
        self.addlink_enabled = criteria.get('addlink', [True])[0]
        portal_types = criteria.get('portal_type', [])
        # During traversal, we are Anonymous User,
        # so we can't do catalog search in update method.
        directory = find_directory(self.context)
        directory_url = directory.absolute_url()
        if len(portal_types) == 1:
            self.addnew_url = '%s/++add++%s' % (directory_url, portal_types[0])
            self.closeOnClick = 'true'
            fti = getUtility(IDexterityFTI, name=portal_types[0])
            self.type_name = fti.Title()
        else:
            self.addnew_url = "%s/@@add-contact" % directory_url
            self.closeOnClick = 'false'
            self.type_name = _(u"Contact")

        self.addlink_label = DMF(u"Add ${name}",
                mapping={'name': self.type_name})

        return super(ContactBaseWidget, self).render()

    def js_extra(self):
        return """
$('#%(id)s-autocomplete').find('.addnew'
    ).prepOverlay({
  subtype: 'ajax',
//filter: common_content_filter,
  formselector: '#form',
  closeselector: '[name="form.buttons.cancel"]',
  noform: 'close',
  config: {
      closeOnClick: %(closeOnClick)s,
      closeOnEsc: %(closeOnClick)s
  }
});
""" % dict(id=self.id, closeOnClick=self.closeOnClick)

class ContactAutocompleteSelectionWidget(ContactBaseWidget, AutocompleteSelectionWidget):
    autoFill = False


class ContactAutocompleteMultiSelectionWidget(ContactBaseWidget, AutocompleteMultiSelectionWidget):
    autoFill = False


@implementer(IFieldWidget)
def ContactAutocompleteFieldWidget(field, request):
    widget = ContactAutocompleteSelectionWidget(request)
    return FieldWidget(field, widget)


@implementer(IFieldWidget)
def ContactAutocompleteMultiFieldWidget(field, request):
    widget = ContactAutocompleteMultiSelectionWidget(request)
    return FieldWidget(field, widget)

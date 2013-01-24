from AccessControl import getSecurityManager
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.component import getUtility
from zope.interface import implementer, implements, Interface
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr

from plone.app.layout.viewlets.interfaces import IBelowContent
from plone.dexterity.interfaces import IDexterityFTI
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.formwidget.autocomplete.widget import (
    AutocompleteMultiSelectionWidget,
    AutocompleteSelectionWidget)
from plone.formwidget.autocomplete.widget import AutocompleteSearch as BaseAutocompleteSearch

from plone.dexterity.i18n import MessageFactory as DMF

from . import _
from .interfaces import (
    IContactAutocompleteWidget,
    IContactAutocompleteSelectionWidget,
    IContactAutocompleteMultiSelectionWidget,
    IContactContent)

class PatchLoadInsideOverlay(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHtmlHeadLinks)

    def render(self):
        return """<script type="text/javascript">
$(document).ready(function() {
  $(document).bind('formOverlayLoadSuccess', function(e, req, myform, api, pb, ajax_parent) {
    ajax_parent.find('div').slice(0, 1).prepend(ajax_parent.find('.portalMessage').detach());
  });
  $(document).bind('loadInsideOverlay', function(e, el, responseText, errorText, api) {
    var el = $(el);
    var o = el.closest('.overlay-ajax');
    var pbo = o.data('pbo');
    var overlay_counter = parseInt(pbo.nt.substring(3, pbo.nt.length));
    o.css({zIndex: 9998+overlay_counter});
  });
  $.plonepopups.fill_autocomplete = function (el, pbo, noform) {
    var objpath = el.find('input[name=objpath]');
    if (objpath.length) {
        data = objpath.val().split('|');
        var input_box = pbo.source.siblings('div').find('.querySelectSearch input');
        formwidget_autocomplete_new_value(input_box, data[0], data[1]);
        input_box.flushCache();
        // trigger change event on newly added input element
        var input = input_box.parents('.querySelectSearch').parent('div').siblings('.autocompleteInputWidget').find('input').last();
        $.plonepopups.add_contact_preview(input);
        input.trigger('change');
    }
    return noform;
  };

  var pendingCall = {timeStamp: null, procID: null};
  $.plonepopups.add_contact_preview = function (input) {
    var path = '/' + input.val().split('/').slice(2).join('/');
    var url = portal_url+path;
    input.siblings('.label')
        .wrapInner('<a href="'+url+'" class="link-tooltip">');
  };

  $(document).delegate('.link-tooltip', 'mouseenter', function() {
    var trigger = $(this);
    if (!trigger.data('tooltip')) {
      if (pendingCall.procID) {
        clearTimeout(pendingCall.procID);
      }
      var timeStamp = new Date();
      var tooltipCall = function() {
          var tip = $('<div class="tooltip pb-ajax" style="display:none">please wait</div>')
                .insertAfter(trigger);
          trigger.tooltip({relative: true, position: "center right"});
          var tooltip = trigger.tooltip();
          tooltip.show();
          var url = trigger.attr('href');
          $.get(url, function(data) {
            tooltip.hide();
            tooltip.getTip().html($('<div />').append(
                    data.replace(/<script(.|\s)*?\/script>/gi, ""))
                .find(common_content_filter));
            if (pendingCall.timeStamp == timeStamp) {
                tooltip.show();
            }
            pendingCall.procID = null;
          });
      }
      pendingCall = {timeStamp: timeStamp,
                     procID: setTimeout(tooltipCall, 500)};
    }
  });
});
</script>
<style type="text/css">
.tooltip {
  overflow: hidden;
}
.tooltip, #calroot {
  z-index: 99999;
}
</style>
"""


class ObjPathViewlet(grok.Viewlet):
    grok.context(IContactContent)
    grok.viewletmanager(IBelowContent)

    def render(self):

        token = '/'.join(self.context.getPhysicalPath())
        if base_hasattr(self.context, 'get_full_title'):
            title = self.context.get_full_title()
        else:
            title = self.context.Title()
        title = title.decode('utf-8')
        return u"""<input type="hidden" name="objpath" value="%s" />""" % (
                    '|'.join([token, title]))


def find_directory(context):
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog.unrestrictedSearchResults(portal_type='directory')
    return results[0].getObject()


class ContactBaseWidget(object):
    implements(IContactAutocompleteWidget)
    noValueLabel = _(u'(nothing)')
    autoFill = False
    display_template = ViewPageTemplateFile('templates/contact_display.pt')
    input_template = ViewPageTemplateFile('templates/contact_input.pt')
    js_callback_template = """
function (event, data, formatted) {
    (function($) {
        var input_box = $(event.target);
        formwidget_autocomplete_new_value(input_box,data[0],data[1]);
        // trigger change event on newly added input element
        var input = input_box.parents('.querySelectSearch').parent('div').siblings('.autocompleteInputWidget').find('input').last();
        $.plonepopups.add_contact_preview(input);
        input.trigger('change');
    }(jQuery));
}
"""

    def tokenToUrl(self, token):
        portal_url = getToolByName(self.context, 'portal_url')()
        return "%s/%s" % (portal_url, self.bound_source.tokenToPath(token))

    def render(self):
        source = self.bound_source
        criteria = source.selectable_filter.criteria
        self.addlink_enabled = criteria.get('addlink', [True])[0]
        portal_types = criteria.get('portal_type', [])
        # During traversal, we are Anonymous User,
        # so we can't do catalog search in update method.
        directory = find_directory(self.context)
        sm = getSecurityManager()
        if not sm.checkPermission("Add portal content", directory):
            self.addlink_enabled = False
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
  filter: common_content_filter+',#viewlet-below-content>*',
  formselector: '#form',
  closeselector: '[name="form.buttons.cancel"]',
  noform: function(el, pbo) {return $.plonepopups.fill_autocomplete(el, pbo, 'close');},
  config: {
      closeOnClick: %(closeOnClick)s,
      closeOnEsc: %(closeOnClick)s
  }
});
""" % dict(id=self.id, closeOnClick=self.closeOnClick)

class ContactAutocompleteSelectionWidget(ContactBaseWidget, AutocompleteSelectionWidget):
    implements(IContactAutocompleteSelectionWidget)


class ContactAutocompleteMultiSelectionWidget(ContactBaseWidget, AutocompleteMultiSelectionWidget):
    implements(IContactAutocompleteMultiSelectionWidget)


@implementer(IFieldWidget)
def ContactAutocompleteFieldWidget(field, request):
    widget = ContactAutocompleteSelectionWidget(request)
    return FieldWidget(field, widget)


@implementer(IFieldWidget)
def ContactAutocompleteMultiFieldWidget(field, request):
    widget = ContactAutocompleteMultiSelectionWidget(request)
    return FieldWidget(field, widget)


class AutocompleteSearch(BaseAutocompleteSearch):
    def __call__(self):

        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()

        query = self.request.get('q', None)
        path = self.request.get('path', None)
        if not query:
            if path is None:
                return ''
            else:
                query = ''

        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        self.context.update()
        source = self.context.bound_source

        if path is not None:
            query = "path:%s %s" % (source.tokenToPath(path), query)

        if query:
            terms = set(source.search(query))
        else:
            terms = set()

        return '\n'.join(["%s|%s" % (t.token, t.title or t.token)
                            for t in sorted(terms, key=lambda t: t.title)])

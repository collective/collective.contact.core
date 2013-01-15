from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer, Interface
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from five import grok

from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.formwidget.autocomplete.widget import (
    AutocompleteMultiSelectionWidget,
    AutocompleteSelectionWidget)


class PatchLoadInsideOverlay(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHtmlHeadLinks)

    def render(self):
        return """<script type="text/javascript">
$(document).ready(function() {
  $(document).bind('loadInsideOverlay', function(e, el, responseText, errorText, api) {
    var el = $(el);
    var o = el.closest('.overlay-ajax');
    var pbo = o.data('pbo');
    var overlay_counter = parseInt(pbo.nt.substring(3));
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

class ContactBaseWidget(object):
    display_template = ViewPageTemplateFile('templates/contact_display.pt')
    input_template = ViewPageTemplateFile('templates/contact_input.pt')

    def js_extra(self):
        source = self.bound_source
        portal_types = source.selectable_filter.criteria.get('portal_type', ())
        if len(portal_types) == 1:
            addview = '++add++%s' % portal_types[0]
            closeOnClick = 'true'
        else:
            addview = "@@add-contact"
            closeOnClick = 'false'
        return """
$('#%(id)s-autocomplete').find('.addcontact'
    ).attr('href', '%(addview)s').prepOverlay({
  subtype: 'ajax',
//filter: common_content_filter,
  formselector: '#form',
  closeselector: '[name="form.buttons.cancel"]',
  config: {
      closeOnClick: %(closeOnClick)s,
      closeOnEsc: %(closeOnClick)s
  }
});

""" % dict(id=self.id, addview=addview, closeOnClick=closeOnClick)

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

from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from plone.formwidget.autocomplete.widget import (
    AutocompleteMultiSelectionWidget,
    AutocompleteSelectionWidget)


class ContactBaseWidget(object):
    display_template = ViewPageTemplateFile('templates/contact_display.pt')
    input_template = ViewPageTemplateFile('templates/contact_input.pt')

    def js_extra(self):
        return """
$('.addcontact').prepOverlay({
  subtype: 'ajax',
  filter: common_content_filter,
  formselector: 'form#addcontact'
});

"""

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

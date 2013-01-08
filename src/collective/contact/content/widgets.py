from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer

from plone.formwidget.autocomplete.widget import (
    AutocompleteMultiSelectionWidget,
    AutocompleteSelectionWidget)


@implementer(IFieldWidget)
def AutocompleteFieldWidget(field, request):
    widget = AutocompleteSelectionWidget(request)
    widget.autoFill = False
    return FieldWidget(field, widget)


@implementer(IFieldWidget)
def AutocompleteMultiFieldWidget(field, request):
    widget = AutocompleteMultiSelectionWidget(request)
    widget.autoFill = False
    return FieldWidget(field, widget)

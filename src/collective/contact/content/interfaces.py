from zope.interface import Interface
from z3c.relationfield.interfaces import IRelationChoice, IRelationList
from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget


class IContactAutocompleteWidget(IAutocompleteWidget):
    """Marker interface for the contact autocomplete widget
    """


class IContactChoice(IRelationChoice):
    """A one to one relation where a choice of target objects is available.
    """


class IContactList(IRelationList):
    """A one to many relation.
    """


class IVCard(Interface):

    def get_vcard(self):
        """Get a vobject.VCard object containing vCard information
        See http://vobject.skyhouseconsulting.com/usage.html#vcards and
            ftp://ftp.rfc-editor.org/in-notes/rfc6350.txt
        """

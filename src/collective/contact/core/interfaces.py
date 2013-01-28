from zope.interface import Interface
from z3c.relationfield.interfaces import IRelationChoice, IRelationList
from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget


class IContactContent(Interface):
    """Base class for collective.contact.core content types"""


class IContactAutocompleteWidget(IAutocompleteWidget):
    """Marker interface for the contact autocomplete widget
    """


class IContactAutocompleteSelectionWidget(IContactAutocompleteWidget):
    """Marker interface for the multi selection contact autocomplete widget
    """


class IContactAutocompleteMultiSelectionWidget(IContactAutocompleteWidget):
    """Marker interface for the selection contact autocomplete widget
    """


class IContactChoice(IRelationChoice):
    """A one to one relation where a choice of target objects is available.
    """


class IContactList(IRelationList):
    """A one to many relation.
    """


class IContactable(Interface):

    def get_contact_details():
        """Returns a dict containing the contact details inherited from the hierarchy"""

    def get_parent_address():
        """Returns the address of the first element in the chain with a relevant address"""


class IVCard(Interface):

    def get_vcard(self):
        """Get a vobject.VCard object containing vCard information
        See http://vobject.skyhouseconsulting.com/usage.html#vcards and
            ftp://ftp.rfc-editor.org/in-notes/rfc6350.txt
        """

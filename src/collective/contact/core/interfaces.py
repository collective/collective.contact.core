from zope.interface import Interface


class IContactable(Interface):
    """Interface for Contactable adapter"""

    def get_contact_details():
        """Returns a dict containing the contact details inherited from the hierarchy"""

    def get_parent_address():
        """Returns the address of the first element in the chain with a relevant address"""


class IVCard(Interface):
    """Interface for VCard"""

    def get_vcard(self):
        """Get a vobject.VCard object containing vCard information
        See http://vobject.skyhouseconsulting.com/usage.html#vcards and
            ftp://ftp.rfc-editor.org/in-notes/rfc6350.txt
        """

from zope.interface import Interface
from zope import schema

from collective.contact.core import _


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


class IContactCoreParameters(Interface):

    person_title_in_title = schema.Bool(title=_(u"Display person title in displayed person's title."),
                                        description=u"",
                                        required=False, default=True)

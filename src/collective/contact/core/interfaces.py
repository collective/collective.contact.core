from zope.interface import Interface
from zope import schema

from collective.contact.core import _


class IContactable(Interface):
    """Interface for Contactable adapter"""

    def get_contact_details(self, keys=(), fallback=True):
        """Returns a dict containing the contact details inherited from the hierarchy
        If keys is set, we only get requested values
        If fallback is False, we don't fallback contact details on objects it is related
        """

    def get_parent_address(self,):
        """Returns the address of the first element in the chain with a relevant address"""


class IVCard(Interface):
    """Interface for VCard"""

    def get_vcard(self):
        """Get a vobject.VCard object containing vCard information
        See http://vobject.skyhouseconsulting.com/usage.html#vcards and
            ftp://ftp.rfc-editor.org/in-notes/rfc6350.txt
        """


class IContactCoreParameters(Interface):

    person_title_in_title = schema.Bool(
        title=_(u"Display person title in displayed person's title."),
        description=u"",
        required=False, default=True)

    use_held_positions_to_search_person = schema.Bool(
        title=_(u"Use held positions to search persons."),
        description=u"",
        required=False, default=True)

    use_description_to_search_person = schema.Bool(
        title=_(u"Use description to search persons."),
        description=u"",
        required=False, default=True)


class IPersonHeldPositions(Interface):
    """Adapter interface to get ordered positions of a person
    adapts person object and layer
    """

    def get_main_position(self):
        """When you have to deal with just one position for the person,
        (for example, you want to notify contacts but only once per person)
        this method gives the main position of the person
        """

    def get_current_positions(self):
        """Give the current positions of the person
        """

    def get_sorted_positions(self):
        """Get sorted positions
        """

from zope.interface import Interface
from zope import schema

from plone.namedfile.field import NamedImage
from plone.supermodel import model

from collective.contact.core import _
from collective.contact.core.schema import ContactChoice
from collective.contact.widget.interfaces import IContactContent
from collective.contact.widget.source import ContactSourceBinder


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

    person_contact_details_private = schema.Bool(
        title=_(u"The person contact details are private and will not be used in other context, like held position."),
        description=u"",
        required=False, default=True)

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

    display_contact_photo_on_organization_view = schema.Bool(
        title=_(u"Display contact photo on organization view (instead person content type icon)."),
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


class IHeldPosition(model.Schema, IContactContent):
    """Interface for HeldPosition content type"""

    position = ContactChoice(
        title=_("Organization/Position"),
        source=ContactSourceBinder(portal_type=("organization", "position")),
        required=True,
    )
    label = schema.TextLine(
        title=_("Additional label"),
        description=_("Additional label with information that does not appear "
                      "on position label"),
        required=False)
    start_date = schema.Date(
        title=_("Start date"),
        required=False,
    )
    end_date = schema.Date(
        title=_("End date"),
        required=False,
    )
    photo = NamedImage(
        title=_("Photo"),
        required=False,
        readonly=True,
    )

    def get_person(self):
        """Returns the person who holds the position
        """

    def get_position(self):
        """Returns the position (if position field is a position)
        """

    def get_organization(self):
        """Returns the first organization related to HeldPosition
        i.e. position field or parent of the position
        """

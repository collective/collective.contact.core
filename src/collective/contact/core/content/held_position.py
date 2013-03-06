from ComputedAttribute import ComputedAttribute

from zope.interface import implements
from zope import schema

from five import grok

from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container
from plone.namedfile.field import NamedImage
from plone.supermodel import model

from collective.contact.core import _
from collective.contact.core.schema import ContactChoice
from collective.contact.core.browser.contactable import Contactable
from collective.contact.widget.source import ContactSourceBinder
from collective.contact.widget.interfaces import IContactContent


def acqproperty(func):
    """Property that manages acquisition"""
    return ComputedAttribute(func, 1)


class IHeldPosition(model.Schema, IContactContent):
    """Interface for HeldPosition content type"""

    start_date = schema.Date(
      title=_("Start date"),
      required=False,
    )
    end_date = schema.Date(
      title=_("End date"),
      required=False,
    )
    position = ContactChoice(
        title=_("Position or organization"),
        addlink=False,
        source=ContactSourceBinder(portal_type=("organization", "position"))
    )
    photo = NamedImage(
        title=_("Photo"),
        required=False,
        readonly=True,
        )

    def get_person():
        """Returns the person who holds the position
        """

    def get_position():
        """Returns the position (if position field is a position)
        """

    def get_organization():
        """Returns the first organization related to HeldPosition
        i.e. position field or parent of the position
        """


class HeldPositionContactableAdapter(Contactable):
    """Contactable adapter for HeldPosition content type"""

    grok.context(IHeldPosition)

    @property
    def person(self):
        return self.context.get_person()

    @property
    def position(self):
        return self.context.get_position()

    @property
    def organizations(self):
        organization = self.context.get_organization()
        return organization.get_organizations_chain()



class HeldPosition(Container):
    """HeldPosition content type
    Links a Position or an Organization to a person in an organization
    """

    implements(IHeldPosition)

    def get_person(self):
        """Returns the person who holds the position
        """
        return self.getParentNode()

    def get_position(self):
        """Returns the position (if position field is a position)
        """
        pos_or_org = self.position.to_object
        if pos_or_org.portal_type == 'position':
            return pos_or_org
        else:
            return None

    def get_organization(self):
        """Returns the first organization related to HeldPosition
        i.e. position field or parent of the position
        """
        pos_or_org = self.position.to_object
        if pos_or_org.portal_type == 'position':
            return pos_or_org.get_organization()
        elif pos_or_org.portal_type == 'organization':
            return pos_or_org

    def Title(self):
        """The held position's title is constituted by the position's
        title and the root organization's title"""
        position = self.position.to_object
        organization = self.get_organization().get_root_organization()
        if position == organization:
            return position.Title()
        else:
            return "%s (%s)" % (position.Title(),
                                organization.Title())

    def get_full_title(self):
        """Returns the 'full title' of the held position.
        It is constituted by the person's who held the position name,
        the root organization and the position name (if any)
        """
        person_name = self.get_person().Title()
        root_organization = self.get_organization().get_root_organization().Title()
        position = self.get_position()
        if position is None:
            return "%s (%s)" % (person_name,
                                root_organization)
        else:
            position_name = position.Title()
            return "%s (%s - %s)" % (person_name,
                                     root_organization,
                                     position_name)

    @acqproperty
    def photo(self):
        """Get photo from Person"""
        person = self.get_person()
        return person.photo


class HeldPositionSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """Schema policy for HeldPosition content type"""

    grok.name("schema_policy_held_position")

    def bases(self, schemaName, tree):
        return (IHeldPosition,)

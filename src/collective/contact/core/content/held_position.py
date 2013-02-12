from zope.interface import implements
from zope import schema

from five import grok

from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container
from plone.supermodel import model

from collective.contact.core import _
from collective.contact.core.schema import ContactChoice
from collective.contact.widget.source import ContactSourceBinder
from collective.contact.core.interfaces import IContactContent
from collective.contact.core.browser.contactable import Contactable


class IHeldPosition(model.Schema, IContactContent):

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

    def get_person():
        """Get the person who helds the position
        """

    def get_position():
        """Get the position (if position field is a position)
        """

    def get_organization():
        """Get the first organization related to HeldPosition
        i.e. position field or parent of the position
        """


class HeldPositionContactableAdapter(Contactable):
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
    """Position held by a person in an organization"""
    implements(IHeldPosition)

    def get_person(self):
        return self.getParentNode()

    def get_position(self):
        pos_or_org = self.position.to_object
        if pos_or_org.portal_type == 'position':
            return pos_or_org
        else:
            return None

    def get_organization(self):
        pos_or_org = self.position.to_object
        if pos_or_org.portal_type == 'position':
            return pos_or_org.get_organization()
        elif pos_or_org.portal_type == 'organization':
            return pos_or_org

    def Title(self):
        return self.position.to_object.Title()

    def get_full_title(self):
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


class HeldPositionSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_held_position")

    def bases(self, schemaName, tree):
        return (IHeldPosition,)

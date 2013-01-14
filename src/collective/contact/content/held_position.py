from zope.interface import implements
from zope import schema
from z3c.relationfield.schema import RelationChoice

from five import grok

from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container
from plone.supermodel import model

from . import _


class IHeldPosition(model.Schema):

    start_date = schema.Date(
      title=_("Start date"),
    )
    end_date = schema.Date(
      title=_("End date")
    )
    position = RelationChoice(
        title=_("Position or organization"),
        source=ObjPathSourceBinder(portal_type=("organization", "position"))
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
            return pos_or_org.getParentNode()
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

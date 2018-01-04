from ComputedAttribute import ComputedAttribute
from Products.CMFPlone.utils import normalizeString, safe_unicode

from z3c.form.interfaces import NO_VALUE
from zope.interface import implements

from five import grok

from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container

from collective.contact.core.browser.contactable import Contactable
from collective.contact.core.interfaces import IHeldPosition


def acqproperty(func):
    """Property that manages acquisition"""
    return ComputedAttribute(func, 1)


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
        return organization and organization.get_organizations_chain() or []


class HeldPosition(Container):
    """HeldPosition content type
    Links a Position or an Organization to a person in an organization
    """

    implements(IHeldPosition)

    use_parent_address = NO_VALUE
    parent_address = NO_VALUE

    def set_title(self, val):
        return

    def get_title(self):
        return self.Title()

    title = property(get_title, set_title)

    def get_person(self):
        """Returns the person who holds the position
        """
        return self.getParentNode()

    def get_position(self):
        """Returns the position (if position field is a position)
        """
        pos_or_org = self.position.to_object
        if pos_or_org is None:
            return None
        elif pos_or_org.portal_type == 'position':
            return pos_or_org
        else:
            return None

    def get_organization(self):
        """Returns the first organization related to HeldPosition
        i.e. position field or parent of the position
        """
        pos_or_org = self.position.to_object
        if pos_or_org is None:
            return None
        elif pos_or_org.portal_type == 'position':
            return pos_or_org.get_organization()
        elif pos_or_org.portal_type == 'organization':
            return pos_or_org

    def Title(self):
        """The held position's title is constituted by the position's
        title, the organization's title and the root organization's title"""
        position = self.position.to_object
        if position is None:  # the reference was removed
            return self.getId()

        organization = self.get_organization()
        root_organization = organization.get_root_organization()
        if position == organization:
            if self.label:
                return "%s (%s) " % (self.label.encode('utf-8'),
                                     position.Title())
            else:
                return organization.Title()
        else:
            if organization == root_organization:
                return "%s (%s)" % (position.Title(),
                                    organization.Title())
            else:
                return "%s, %s (%s)" % (position.Title(),
                                        organization.Title(),
                                        root_organization.Title())

    def get_full_title(self):
        """Returns the 'full title' of the held position.
        It is constituted by the person's who held the position name,
        the root organization and the position name (if any)
        """
        person_name = self.get_person_title()
        if self.position.to_object is None:  # the reference was removed
            return u"%s (%s)" % (person_name, self.getId())

        position = self.get_position()
        organization = self.get_organization()
        root_organization = organization.get_root_organization().title
        if position is None and not self.label:
            return u"%s (%s)" % (person_name,
                                 root_organization)
        elif position is None and self.label:
            position_name = self.label
            return u"%s (%s - %s)" % (person_name,
                                      root_organization,
                                      position_name)
        else:
            position_name = position.title
            return u"%s (%s - %s)" % (person_name,
                                      root_organization,
                                      position_name)

    def get_person_title(self):
        person = self.get_person()
        if person is None:
            return u""
        return person.get_title()

    def get_sortable_title(self):
        person = self.get_person()
        if person is None:
            return u""
        sortable_fullname = person.get_sortable_title()
        held_position_title = self.Title()
        return u"%s-%s" % (
            sortable_fullname,
            normalizeString(safe_unicode(held_position_title))
        )

    @acqproperty
    def person_title(self):
        person = self.get_person()
        if person is None:
            return u""
        return person.person_title

    @acqproperty
    def photo(self):
        """Get photo from Person"""
        person = self.get_person()
        if person is None:
            return None
        return person.photo


class HeldPositionSchemaPolicy(grok.GlobalUtility,
                               DexteritySchemaPolicy):
    """Schema policy for HeldPosition content type"""

    grok.name("schema_policy_held_position")

    def bases(self, schemaName, tree):
        return (IHeldPosition,)

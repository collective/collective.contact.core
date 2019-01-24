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
        return safe_unicode(self.Title())

    title = property(get_title, set_title)

    def get_label(self):
        """Returns the held_position label.
           Made to be overrided."""
        return self.label

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

    def Title(self, separator=u' / ', first_index=0):
        """The held position's title is constituted by the position's
           title (or held_position label) and the organizations chain."""
        position = self.position.to_object
        if position is None:  # the reference was removed
            return self.getId()

        position = self.get_position()
        organization = self.get_organization()
        label = self.get_label()
        if position is None and not label:
            return "(%s)" % organization.get_full_title(separator=separator, first_index=first_index).encode('utf8')
        # we display the position title or the label
        position_title = label or position.title
        return "%s (%s)" % (position_title.encode('utf8'),
                            organization.get_full_title(separator=separator, first_index=first_index).encode('utf8'))

    def get_full_title(self, separator=u' / ', first_index=0):
        """Returns the 'title' and include person name."""
        person_name = self.get_person_title()
        title = self.Title(separator=separator, first_index=first_index).decode('utf8')
        if title[0:1] == '(':
            return u"%s %s" % (person_name, title)
        else:
            return u"%s, %s" % (person_name, title)

    def get_person_title(self, include_person_title=True):
        person = self.get_person()
        if person is None:
            return u""
        return person.get_title(include_person_title=include_person_title)

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

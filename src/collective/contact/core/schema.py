from zope.interface import implements
from z3c.relationfield.schema import RelationChoice, RelationList

from .interfaces import IContactChoice, IContactList
from .source import ContactSourceBinder


class ContactList(RelationList):
    implements(IContactList)

    def __init__(self, *args, **kwargs):
        if not 'value_type' in kwargs:
            kwargs['value_type'] = ContactChoice()
        super(ContactList, self).__init__(*args, **kwargs)


class ContactChoice(RelationChoice):
    implements(IContactChoice)

    def __init__(self, *args, **kwargs):
        if not ('values' in kwargs or 'vocabulary' in kwargs or 'source' in kwargs):
            kwargs['source'] = ContactSourceBinder(
                            portal_type=('organization', 'person', 'held_position'))
        super(ContactChoice, self).__init__(*args, **kwargs)

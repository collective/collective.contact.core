from zope.interface import implements
from z3c.relationfield.schema import RelationChoice, RelationList

from .interfaces import IContactChoice, IContactList


class ContactList(RelationList):
    implements(IContactList)


class ContactChoice(RelationChoice):
    implements(IContactChoice)

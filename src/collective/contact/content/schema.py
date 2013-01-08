from zope.interface import implements
from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree import ObjPathSourceBinder

from .interfaces import IContactChoice, IContactList


class ContactList(RelationList):
    implements(IContactList)

    def __init__(self, *args, **kwargs):
        super(ContactList, self).__init__(value_type=ContactChoice(), *args, **kwargs)


class ContactChoice(RelationChoice):
    implements(IContactChoice)

    def __init__(self, *args, **kwargs):
        if not ('source' in kwargs or 'vocabulary' in kwargs or 'source' in kwargs):
            kwargs['source'] = ObjPathSourceBinder(
                            portal_type=('organization', 'person', 'held_position'))
        super(RelationChoice, self).__init__(*args, **kwargs)

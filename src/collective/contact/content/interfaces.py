from z3c.relationfield.interfaces import IRelationChoice, IRelationList


class IContactChoice(IRelationChoice):
    """A one to one relation where a choice of target objects is available.
    """

class IContactList(IRelationList):
    """A one to many relation.
    """

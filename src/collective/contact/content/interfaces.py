from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from . import _

class IStructure(model.Schema):
    model.load("models/structure.xml")


class IHeldPosition(model.Schema):
    model.load("models/held_position.xml")

    structure = RelationChoice(
            title=_(u"Structure"),
            source=ObjPathSourceBinder(portal_type=("structure", "position")),
            required=False,
        )

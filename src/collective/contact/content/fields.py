import plone.supermodel.exportimport
import z3c.relationfield.schema


# Field import/export handlers
RelationChoiceHandler = plone.supermodel.exportimport.ChoiceHandler(z3c.relationfield.schema.RelationChoice)

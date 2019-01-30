from collective.contact.widget.interfaces import IContactContent


try:  # TODO: read with plone5 because of grok...
    import plone.supermodel.exportimport
    import z3c.relationfield.schema
    from Acquisition import aq_get
    from plone.app.linkintegrity.handlers import referencedObjectRemoved as baseReferencedObjectRemoved
    from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
    from zc.relation.interfaces import ICatalog
    from zope import component
    from zope.intid import IIntIds
except ImportError:
    pass

try:
    from plone.app.referenceablebehavior.referenceable import IReferenceable
except ImportError:
    from zope.interface import Interface


    class IReferenceable(Interface):
        pass


def referenceRemoved(obj, event, toInterface=IContactContent):
    """Store information about the removed link integrity reference.
    """
    # inspired from z3c/relationfield/event.py:breakRelations
    # and plone/app/linkintegrity/handlers.py:referenceRemoved
    # if the object the event was fired on doesn't have a `REQUEST` attribute
    # we can safely assume no direct user action was involved and therefore
    # never raise a link integrity exception...
    request = aq_get(obj, 'REQUEST', None)
    if not request:
        return
    storage = ILinkIntegrityInfo(request)

    catalog = component.queryUtility(ICatalog)
    intids = component.queryUtility(IIntIds)
    if catalog is None or intids is None:
        return

    # find all relations that point to us
    obj_id = intids.queryId(obj)
    if obj_id is None:
        return

    rels = list(catalog.findRelations({'to_id': obj_id}))
    for rel in rels:
        if toInterface.providedBy(rel.to_object):
            storage.addBreach(rel.from_object, rel.to_object)


def referencedObjectRemoved(obj, event):
    if not IReferenceable.providedBy(obj):
        baseReferencedObjectRemoved(obj, event)


# Field import/export handlers
RelationChoiceHandler = plone.supermodel.exportimport.ChoiceHandler(z3c.relationfield.schema.RelationChoice)

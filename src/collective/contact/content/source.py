from zope.schema.vocabulary import SimpleTerm
from plone.formwidget.contenttree.source import PathSourceBinder, ObjPathSource


class ContactSource(ObjPathSource):

    def getTermByBrain(self, brain, real_value=True):
        if real_value:
            value = brain._unrestrictedGetObject()
        else:
            value = brain.getPath()[len(self.portal_path):]
        # TODO avoid to wake up object, create a get_full_title brain metadada
        if hasattr(brain.getObject(), "get_full_title"):
            full_title = brain.getObject().get_full_title()
            return SimpleTerm(value, token=brain.getPath(), title=full_title)
        else:
            return SimpleTerm(value, token=brain.getPath(), title=brain.Title or
                          brain.id)


class ContactSourceBinder(PathSourceBinder):
    path_source = ContactSource

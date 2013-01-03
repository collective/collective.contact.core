from Acquisition import aq_parent
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.globalrequest import getRequest


class NoDirectoryFound(Exception):
    """No directory found"""


def get_directory(context):
    """Get collective.contact.content Directory"""
    parent = context
    while parent.portal_type != "directory":
        parent = aq_parent(parent)
        if getattr(parent, 'portal_type', None) is None:
            raise NoDirectoryFound
    return parent


def get_vocabulary(schema_list):
    terms = []
    for item in schema_list:
        term = SimpleVocabulary.createTerm(item['token'],
                                           item['token'],
                                           item['name'])
        terms.append(term)
    return SimpleVocabulary(terms)


class PositionTypes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        try:
            directory = get_directory(context)
            return get_vocabulary(directory.position_types)
        except NoDirectoryFound:
            return SimpleVocabulary([])


class OrganizationTypesOrLevels(object):
    implements(IVocabularyFactory)

    def get_container_type(self, context):
        if "++add++organization" in getRequest().getURL():
            # creation mode
            return context.portal_type
        else:
            # edit or view mode
            return context.getParentNode().portal_type

    def __call__(self, context):
        try:
            directory = get_directory(context)
            container_type = self.get_container_type(context)
            if container_type == 'directory':
                return get_vocabulary(directory.organization_types)
            elif container_type == 'organization':
                return get_vocabulary(directory.organization_levels)
        except NoDirectoryFound:
            return SimpleVocabulary([])

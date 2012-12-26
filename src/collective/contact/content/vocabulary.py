from Acquisition import aq_parent
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory


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

    def is_root(self, context):
        # TODO : problem : context is parent during creation and item after
        if hasattr(context, 'is_root_organization'):
            return context.is_root_organization
        else:
            container_type_name = context.getPortalTypeName()
            if container_type_name == 'directory':
                return True
            elif container_type_name == 'organization':
                return False

    def __call__(self, context):
        try:
            directory = get_directory(context)
            # TODO: is there a better way to do this ?
            if self.is_root(context):
                return get_vocabulary(directory.organization_types)
            else:
                return get_vocabulary(directory.organization_levels)
        except NoDirectoryFound:
            return SimpleVocabulary([])

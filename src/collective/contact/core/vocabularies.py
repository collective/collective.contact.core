from . import _
from Acquisition import aq_parent
from collective.contact.core import logger
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class NoDirectoryFound(Exception):
    """No directory found"""


def get_directory(context):
    """Get collective.contact.core Directory"""
    parent = context
    if not parent:
        raise NoDirectoryFound
    while parent.portal_type != "directory":
        parent = aq_parent(parent)
        if getattr(parent, 'portal_type', None) is None:
            raise NoDirectoryFound
    return parent


def get_vocabulary(schema_list):
    terms = []
    tokens = set()
    for item in schema_list:
        token = item['token']
        if token in tokens:
            logger.error("Duplicated value in vocabulary: {}".format(token))
            continue

        tokens.add(token)
        term = SimpleVocabulary.createTerm(token,
                                           token,
                                           item['name'])
        terms.append(term)
    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def PositionTypes(context):

    try:
        directory = get_directory(context)
        return get_vocabulary(directory.position_types)
    except NoDirectoryFound:
        return SimpleVocabulary([])


@implementer(IVocabularyFactory)
class OrganizationTypesOrLevels(object):

    def get_container_type(self, context):
        request = context.REQUEST
        if request and "++add++organization" in request.getURL():
            # creation mode
            return context.portal_type
        else:
            # edit or view mode
            return context.getParentNode().portal_type

    def __call__(self, context):
        try:
            directory = get_directory(context)
            container_type = self.get_container_type(context)
            if container_type == 'organization':
                return get_vocabulary(directory.organization_levels)
            else:
                # directory, folder or anything else
                return get_vocabulary(directory.organization_types)
        except NoDirectoryFound:
            return SimpleVocabulary([])


OrganizationTypesOrLevelsFactory = OrganizationTypesOrLevels()


@provider(IVocabularyFactory)
def Genders(context):

    terms = []
    genders = {'M': _("Male"), 'F': _("Female")}
    for (token, value) in genders.items():
        term = SimpleVocabulary.createTerm(token, token, value)
        terms.append(term)
    return SimpleVocabulary(terms)

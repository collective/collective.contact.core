from Acquisition import aq_parent
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory


class OrganizationTypes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        parent = context
        while parent.portal_type != "directory":
            parent = aq_parent(parent)

        terms = []
        for line in parent.organization_types.split('\n'):
            value, title = line.split('|')
            terms.append(SimpleVocabulary.createTerm(
                value, value, title))
        return SimpleVocabulary(terms)

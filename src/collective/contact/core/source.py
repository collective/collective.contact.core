from zope.schema.vocabulary import SimpleTerm

from Products.ZCTextIndex.ParseTree import ParseError

from plone.formwidget.contenttree.source import PathSourceBinder, ObjPathSource
from Products.CMFPlone.utils import base_hasattr


def parse_query(query, path_prefix=""):
    """Copied from plone.app.vocabularies.catalog.parse_query
    but depth=1 removed.
    """
    query_parts = query.split()
    query = {'SearchableText': []}
    for part in query_parts:
        if part.startswith('path:'):
            path = part[5:]
            query['path'] = {'query': path}
        else:
            query['SearchableText'].append(part)
    text = " ".join(query['SearchableText'])
    for char in '?-+*()':
        text = text.replace(char, ' ')
    query['SearchableText'] = " AND ".join(x + "*" for x in text.split())
    if 'path' in query:
        if query['SearchableText'] == '':
            del query['SearchableText']
#            query["path"]["depth"] = 1
        query["path"]["query"] = path_prefix + query["path"]["query"]
    return query


class ContactSource(ObjPathSource):

    def getTermByBrain(self, brain, real_value=True):
        if real_value:
            value = brain._unrestrictedGetObject()
        else:
            value = brain.getPath()[len(self.portal_path):]
        # TODO avoid to wake up object, create a get_full_title brain metadada
        if base_hasattr(brain.getObject(), "get_full_title"):
            full_title = brain.getObject().get_full_title()
            return SimpleTerm(value, token=brain.getPath(), title=full_title)
        else:
            return SimpleTerm(value, token=brain.getPath(), title=brain.Title or
                          brain.id)

    def tokenToPath(self, token):
        """For token='/Plone/a/b', return '/a/b'
        """
        return '/'+'/'.join(token.split('/')[2:])

    def search(self, query, limit=20):
        """Copy from plone.formwidget.contenttree.source,
        to be able to use a modified version of parse_query.
        """
        catalog_query = self.selectable_filter.criteria.copy()
        catalog_query.update(parse_query(query, self.portal_path))

        if limit and 'sort_limit' not in catalog_query:
            catalog_query['sort_limit'] = limit

        try:
            results = (self.getTermByBrain(brain, real_value=False)
                       for brain in self.catalog(**catalog_query))
        except ParseError:
            return []

        return results


class ContactSourceBinder(PathSourceBinder):
    path_source = ContactSource

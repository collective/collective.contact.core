from plone.dexterity.browser.view import DefaultView
from plone import api


class Directory(DefaultView):

    def update(self):
        super(Directory, self).update()
        directory_path = '/'.join(self.context.getPhysicalPath())
        search_path = {'query': directory_path, 'depth': 1}
        catalog = api.portal.get_tool('portal_catalog')
        self.persons = catalog.searchResults(portal_type="person",
                                             path=search_path)
        self.organizations = catalog.searchResults(portal_type="organization",
                                                   path=search_path)

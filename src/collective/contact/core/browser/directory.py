from plone.dexterity.browser.view import DefaultView


class Directory(DefaultView):

    def update(self):
        super(Directory, self).update()
        self.persons = self.context.objectValues('person')
        self.organizations = self.context.objectValues('organization')

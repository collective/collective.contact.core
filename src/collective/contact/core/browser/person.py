from five import grok

from Products.CMFCore.utils import getToolByName

from collective.contact.core.browser import TEMPLATES_DIR
from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.content.person import IPerson


grok.templatedir(TEMPLATES_DIR)


class Person(BaseView):

    def update(self):
        super(Person, self).update()


class HeldPositions(grok.View):
    """Displays held positions list"""
    grok.name('heldpositions')
    grok.template('heldpositions')
    grok.context(IPerson)

    held_positions = ''

    def update(self):
        person = self.context
        catalog = getToolByName(person, 'portal_catalog')
        context_path = '/'.join(person.getPhysicalPath())
        held_positions = []
        for brain in catalog.searchResults(portal_type='held_position',
                                           path={'query': context_path, 'depth': 1}):
            held_position = {}
            obj = brain.getObject()
            held_position['label'] = obj.label
            held_position['start_date'] = obj.start_date
            held_position['end_date'] = obj.end_date
            #held_position['phone'] = obj.phone
            #held_position['email'] = obj.email
            held_position['object'] = obj
            held_position['organization'] = obj.get_organization().get_root_organization()
            held_positions.append(held_position)
        self.held_positions = held_positions

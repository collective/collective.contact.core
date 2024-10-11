from AccessControl import getSecurityManager
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.browser.utils import date_to_DateTime
from collective.contact.core.interfaces import IContactable
from collective.contact.core.interfaces import IPersonHeldPositions
from Products.Five import BrowserView
from zope.component import queryMultiAdapter


class Person(BaseView):

    def update(self):
        super(Person, self).update()
        # Do not show person contact details
        # if they are the same as the main held position
        contactable_held_position = IContactable(self.context).held_position
        if IContactDetails.providedBy(contactable_held_position) and not IContactDetails.providedBy(self.context):
            self.show_contact_details = False
        else:
            self.show_contact_details = True


class HeldPositions(BrowserView):
    """Displays held positions list"""
    held_positions = ''

    def __call__(self):
        person = self.context
        sm = getSecurityManager()
        held_positions = []
        for obj in IPersonHeldPositions(person).get_sorted_positions():
            held_position = {}
            held_position['title'] = obj.Title()
            if obj.start_date is not None:
                start_date = date_to_DateTime(obj.start_date)
                held_position['start_date'] = person.toLocalizedTime(start_date)
            else:
                held_position['start_date'] = None

            if obj.end_date is not None:
                end_date = date_to_DateTime(obj.end_date)
                held_position['end_date'] = person.toLocalizedTime(end_date)
            else:
                held_position['end_date'] = None

            # held_position['phone'] = obj.phone
            # held_position['email'] = obj.email
            held_position['object'] = obj
            organization = obj.get_organization()

            icons = queryMultiAdapter((obj, self.request), name="iconresolver")
            held_position['icon'] = icons.url("file-earmark-person-fill")
            held_position['organization'] = organization if organization else None
            held_position['can_edit'] = sm.checkPermission('Modify portal content', obj)
            held_position['can_delete'] = sm.checkPermission('Delete objects', obj)
            held_positions.append(held_position)

        self.held_positions = held_positions
        return super(HeldPositions, self).__call__()

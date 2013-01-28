from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.browser.utils import get_ttw_fields
from collective.contact.core.interfaces import IContactable


class Position(BaseView):

    name = ''
    type = ''
    organizations = []

    def update(self):
        super(Position, self).update()
        self.position = self.context
        position = self.position
        self.name = position.Title()
        factory = getUtility(IVocabularyFactory, "PositionTypes")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(position.position_type).title

        contactable = IContactable(position)
        self.organizations = contactable.organizations

        contact_details = contactable.get_contact_details()
        self.email = contact_details['email']
        self.phone = contact_details['phone']
        self.cell_phone = contact_details['cell_phone']
        self.im_handle = contact_details['im_handle']
        self.address = contact_details['address']

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(position)

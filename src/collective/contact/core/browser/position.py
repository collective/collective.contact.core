from AccessControl import getSecurityManager
from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.interfaces import IContactable
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class Position(BaseView):

    def update(self):
        super(Position, self).update()
        self.position = self.context
        position = self.position
        factory = getUtility(IVocabularyFactory, "PositionTypes")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(position.position_type).title

        contactable = IContactable(position)
        self.organizations = contactable.organizations

        sm = getSecurityManager()
        self.can_add = sm.checkPermission('Add portal content', self.context)

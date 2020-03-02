# -*- coding: utf-8 -*-
from collective.contact.core.browser.utils import get_ttw_fields
from Products.Five import BrowserView


class TTWFields(BrowserView):
    """Show fields that were added TTW
    """

    def update(self):
        contact_view = self.context.unrestrictedTraverse('view')
        contact_view.update()
        self.widgets = contact_view.widgets
        ttw_fields = get_ttw_fields(self.context)
        self.ttw_fields = [
            field for field in ttw_fields if field in self.widgets.keys()]

    def __call__(self):
        self.update()
        return super(TTWFields, self).__call__()

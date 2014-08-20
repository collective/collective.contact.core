from five import grok

from zope.interface import Interface

from collective.contact.core.browser.utils import get_ttw_fields
from collective.contact.core.browser import TEMPLATES_DIR


grok.templatedir(TEMPLATES_DIR)


class TTWFields(grok.View):
    """Show fields that were added TTW
    """
    grok.name('ttwfields')
    grok.template('ttwfields')
    grok.context(Interface)

    def update(self):
        contact_view = self.context.unrestrictedTraverse('view')
        contact_view.update()
        self.widgets = contact_view.widgets
        ttw_fields = get_ttw_fields(self.context)
        self.ttw_fields = [field for field in ttw_fields if field in self.widgets.keys()]

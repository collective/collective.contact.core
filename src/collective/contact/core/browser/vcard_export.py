from five import grok

from collective.contact.core.interfaces import IVCard
from collective.contact.core.content.held_position import IHeldPosition


class ContactVCF(grok.View):
    grok.name('contact.vcf')
    grok.context(IHeldPosition)
    grok.require("zope2.View")

    def render(self):
        self.request.response.setHeader(
            'Content-type', "text/x-vCard; charset=utf-8")
        content_disposition = 'attachment; filename=%s.vcf' % (self.context.id)
        self.request.response.setHeader(
            'Content-Disposition', content_disposition)
        vcard_provider = IVCard(self.context)
        vcard = vcard_provider.get_vcard()
        return vcard.serialize()

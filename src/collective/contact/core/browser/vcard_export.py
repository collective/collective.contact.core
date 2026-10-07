from collective.contact.core.interfaces import IVCard
from Products.Five import BrowserView


class ContactVCF(BrowserView):

    def __call__(self):
        self.request.response.setHeader(
            'Content-type', "text/x-vCard; charset=utf-8")
        content_disposition = 'attachment; filename=%s.vcf' % (self.context.id)
        self.request.response.setHeader(
            'Content-Disposition', content_disposition)
        vcard_provider = IVCard(self.context)
        vcard = vcard_provider.get_vcard()
        return vcard.serialize()

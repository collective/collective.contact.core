from five import grok
import vobject

from collective.contact.content.interfaces import IVCard
from collective.contact.content.content.held_position import IHeldPosition,\
                                                             HeldPosition


class HeldPositionVCard(grok.Adapter):
    grok.implements(IHeldPosition)
    grok.context(HeldPosition)
    grok.provides(IVCard)

    def __init__(self, context):
        self.context = context

    def get_vcard(self):
        vcard = vobject.vCard()
        person = self.context.getParentNode()
        vcard.add('n')
        firstname = unicode(person.firstname or '')
        lastname = unicode(person.lastname or '')
        person_title = unicode(person.person_title or '')
        vcard.n.value = vobject.vcard.Name(prefix=person_title,
                                           family=lastname,
                                           given=firstname)
        vcard.add('fn')
        vcard.fn.value = ' '.join([e for e in (firstname, lastname) if e])

        if person.birthday is not None:
            vcard.add('bday')
            vcard.bday.value = person.birthday.isoformat()

        position = self.context.get_position()
        if position is not None:
            position_name = unicode(position.Title())
            vcard.add('role')
            vcard.role.value = position_name
            vcard.add('title')
            vcard.title.value = position_name

        organization = self.context.get_organization()
        vcard.add('org')
        orgs = organization.get_organizations_titles()
        vcard.org.value = [unicode(org) for org in orgs]

        if person.email is not None:
            vcard.add('email')
            vcard.email.type_param = 'INTERNET'
            vcard.email.value = person.email

        # if we don't have relevant address information, we don't need address
        if person.city is not None or \
           person.country is not None or \
           person.region is not None:
            vcard.add('adr')
            country = unicode(person.country or '')
            region = unicode(person.region or '')
            street = unicode(person.street or '')
            city = unicode(person.city or '')
            additional = unicode(person.additional_address_details or '')
            vcard.adr.value = vobject.vcard.Address(street=street,
                                                    city=city,
                                                    region=region,
                                                    code=person.zip_code or '',
                                                    country=country,
                                                    box=person.number or '',
                                                    extended=additional)
        if person.phone is not None:
            vcard.add('tel')
            vcard.tel.type_param = 'WORK'
            vcard.tel.value = person.phone
        if person.cell_phone is not None:
            vcard.add('tel')
            last_item = len(vcard.tel_list) - 1
            vcard.tel_list[last_item].type_param = 'CELL'
            vcard.tel_list[last_item].value = person.cell_phone

        #vcard.add('photo')
        #vcard.photo.value = person.photo

#        if person.latitude is not None and \
#           person.longitude is not None:
#            vcard.add('geo')
#            vcard.geo.value = "%.2f;%.2f" % (person.latitude, person.longitude)

        return vcard

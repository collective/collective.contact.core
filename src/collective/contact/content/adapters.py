from five import grok
import vobject

from collective.contact.vcard.interfaces import IVCard
from collective.contact.content.held_position import IHeldPosition,\
                                                     HeldPosition


def get_organization_vcard(organization):
    return ';'.join(organization.get_organizations_titles())


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
        firstname = person.firstname or ''
        lastname = person.lastname or ''
        person_title = person.person_title
        vcard.n.value = vobject.vcard.Name(prefix=person_title or '',
                                           family=lastname,
                                           given=firstname)
        vcard.add('fn')
        vcard.fn.value = ' '.join([e for e in (firstname, lastname) if e])

        if person.birthday is not None:
            vcard.add('bday')
            vcard.bday.value = person.birthday.isoformat()

        position = self.context.get_position()
        if position is not None:
            position_name = position.Title()
            vcard.add('role')
            vcard.role.value = position_name
            vcard.add('title')
            vcard.title.value = position_name

        organization = self.context.get_organization()
        vcard.add('org')
        vcard.org.value = get_organization_vcard(organization)

        if person.email is not None:
            vcard.add('email')
            vcard.email.type_param = 'INTERNET'
            vcard.email.value = person.email

        # if we don't have relevant address information, we don't need address
        if person.city is not None or \
           person.country is not None or \
           person.region is not None:
            vcard.add('adr')
            vcard.adr.value = vobject.vcard.Address(street=person.street or '',
                                                    city=person.city or '',
                                                    region=person.region or '',
                                                    code=person.zip_code or '',
                                                    country=person.country or '',
                                                    box=person.number or '',
                                                    extended=person.additional_address_details or '')
        if person.phone is not None:
            vcard.add('tel')
            vcard.tel.type_param = 'WORK'
            vcard.tel.value = person.phone
        if person.cell_phone is not None:
            vcard.add('tel')
            last_item = len(vcard.tel_list)-1
            vcard.tel_list[last_item].type_param = 'CELL'
            vcard.tel_list[last_item].value = person.cell_phone
        #vcard.add('photo')
        #vcard.photo.value = person.photo

#        if person.latitude is not None and \
#           person.longitude is not None:
#            vcard.add('geo')
#            vcard.geo.value = "%.2f;%.2f" % (person.latitude, person.longitude)

        return vcard

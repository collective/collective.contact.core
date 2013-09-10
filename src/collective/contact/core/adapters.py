from five import grok
import vobject

from Products.CMFPlone.utils import safe_unicode

from collective.contact.core.interfaces import IVCard, IContactable
from collective.contact.core.content.held_position import IHeldPosition,\
                                                             HeldPosition
from collective.contact.core.behaviors import IBirthday


class HeldPositionVCard(grok.Adapter):
    grok.implements(IHeldPosition)
    grok.context(HeldPosition)
    grok.provides(IVCard)

    def __init__(self, context):
        self.context = context

    def get_vcard(self):
        vcard = vobject.vCard()
        held_position = self.context
        contactable = IContactable(held_position)
        person = contactable.person
        position = contactable.position
        organizations = contactable.organizations
        contact_details = contactable.get_contact_details()

        vcard.add('n')
        firstname = safe_unicode(person.firstname or '', encoding='utf8')
        lastname = safe_unicode(person.lastname or '', encoding='utf8')
        person_title = safe_unicode(person.person_title or '', encoding='utf8')
        vcard.n.value = vobject.vcard.Name(prefix=person_title,
                                           family=lastname,
                                           given=firstname)
        vcard.add('fn')
        vcard.fn.value = ' '.join([e for e in (firstname, lastname) if e])

        if IBirthday.providedBy(person) and person.birthday is not None:
            vcard.add('bday')
            vcard.bday.value = person.birthday.isoformat()

        if position is not None:
            position_name = safe_unicode(position.Title(), encoding='utf8')
            vcard.add('role')
            vcard.role.value = position_name
            vcard.add('title')
            vcard.title.value = position_name

        vcard.add('org')
        vcard.org.value = [safe_unicode(org.Title(),
                                        encoding='utf8') for org in organizations]

        email = contact_details['email']
        if email:
            vcard.add('email')
            vcard.email.type_param = 'INTERNET'
            vcard.email.value = email

        phone = contact_details['phone']
        if phone:
            vcard.add('tel')
            vcard.tel.type_param = 'WORK'
            vcard.tel.value = phone

        cell_phone = contact_details['cell_phone']
        if cell_phone:
            vcard.add('tel')
            last_item = len(vcard.tel_list) - 1
            vcard.tel_list[last_item].type_param = 'CELL'
            vcard.tel_list[last_item].value = cell_phone

        im_handle = contact_details['im_handle']
        if im_handle:
            vcard.add('impp')
            vcard.impp.value = im_handle

        address = contact_details['address']

        # if we don't have relevant address information, we don't need address
        if address:
            vcard.add('adr')
            country = safe_unicode(address['country'], encoding='utf8')
            region = safe_unicode(address['region'], encoding='utf8')
            zip_code = safe_unicode(address['zip_code'], encoding='utf8')
            city = safe_unicode(address['city'], encoding='utf8')
            street = safe_unicode(address['street'], encoding='utf8')
            number = safe_unicode(address['number'], encoding='utf8')
            additional = safe_unicode(address['additional_address_details'],
                                      encoding='utf8')
            vcard.adr.value = vobject.vcard.Address(street=street,
                                                    city=city,
                                                    region=region,
                                                    code=zip_code,
                                                    country=country,
                                                    box=number,
                                                    extended=additional)

        # TODO ?
        #vcard.add('photo')
        #vcard.photo.value = person.photo

#        if person.latitude is not None and \
#           person.longitude is not None:
#            vcard.add('geo')
#            vcard.geo.value = "%.2f;%.2f" % (person.latitude, person.longitude)

        return vcard

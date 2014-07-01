import datetime
import vobject

from zope.interface import Interface, implements
from five import grok

from Products.CMFPlone.utils import safe_unicode
from plone import api

from collective.contact.core.interfaces import IVCard, IContactable,\
    IPersonHeldPositions
from collective.contact.core.content.held_position import IHeldPosition,\
                                                             HeldPosition
from collective.contact.core.content.organization import IOrganization,\
                                                             Organization
from collective.contact.core.behaviors import IBirthday


class ContactableVCard:

    def __init__(self, context):
        self.context = context

    def get_vcard(self):
        vcard = vobject.vCard()
        contactable = IContactable(self.context)
        contact_details = contactable.get_contact_details()

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

        return vcard


class ContactDetailsVCard(grok.Adapter, ContactableVCard):
    grok.context(Interface)
    grok.provides(IVCard)

    def __init__(self, context):
        self.context = context

    def get_vcard(self):
        vcard = ContactableVCard.get_vcard(self)
        vcard.add('fn')
        vcard.fn.value = self.context.Title()
        vcard.add('n')
        vcard.n.value = vobject.vcard.Name(self.context.Title())
        return vcard


class HeldPositionVCard(grok.Adapter, ContactableVCard):
    grok.implements(IHeldPosition)
    grok.context(HeldPosition)
    grok.provides(IVCard)

    def __init__(self, context):
        self.context = context

    def get_vcard(self):
        vcard = ContactableVCard.get_vcard(self)

        vcard.add('kind')
        vcard.kind.value = "individual"

        held_position = self.context
        contactable = IContactable(held_position)
        person = contactable.person
        position = contactable.position
        organizations = contactable.organizations

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

        # TODO ?
        # vcard.add('photo')
        # vcard.photo.value = person.photo

#        if person.latitude is not None and \
#           person.longitude is not None:
#            vcard.add('geo')
#            vcard.geo.value = "%.2f;%.2f" % (person.latitude, person.longitude)

        return vcard


class OrganizationVCard(grok.Adapter, ContactableVCard):
    grok.implements(IOrganization)
    grok.context(Organization)
    grok.provides(IVCard)

    def __init__(self, context):
        self.context = context

    def get_vcard(self):
        vcard = ContactableVCard.get_vcard(self)

        vcard.add('kind')
        vcard.kind.value = "org"

        organization = self.context
        vcard.add('n')
        vcard.n.value = vobject.vcard.Name(organization.Title())
        vcard.add('fn')
        vcard.fn.value = organization.Title()

        return vcard


def sort_closed_positions(position1, position2):
    if position1.end_date == position2.end_date:
        return 0
    elif not position1.end_date:
        # position without end date is greater
        return 1
    elif not position2.end_date:
        return -1
    else:
        return cmp(position1.end_date, position2.end_date)


class PersonHeldPositionsAdapter(object):
    implements(IPersonHeldPositions)

    def __init__(self, person):
        self.person = person

    def get_main_position(self):
        """First active current position in container
        if there is no active position, select first inactive one
        """
        current_positions = self.get_current_positions()
        if not current_positions:
            return None

        for position in current_positions:
            if api.content.get_state(position) == 'active':
                return position
        else:
            return current_positions[0]

    def get_current_positions(self):
        """Get not ended positions
        """
        positions = self.person.get_held_positions()
        return tuple([p for p in positions
                      if (not p.end_date or p.end_date > datetime.date.today())])

    def get_closed_positions(self):
        """Get closed positions by descending order of end date
        """
        all_positions = self.person.get_held_positions()
        active_positions = self.get_current_positions()
        closed_positions = [p for p in all_positions if p not in active_positions]
        closed_positions.sort(cmp=sort_closed_positions, reverse=True)
        return tuple(closed_positions)

    def get_sorted_positions(self):
        return self.get_current_positions() + self.get_closed_positions()

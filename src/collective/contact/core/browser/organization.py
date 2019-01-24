# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.browser.utils import date_to_DateTime
from collective.contact.core.browser.utils import get_valid_url
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.interfaces import IContactable
from collective.contact.core.interfaces import IContactCoreParameters
from five import grok
from plone import api
from Products.Five import BrowserView


ADDNEW_OVERLAY = """
<script type="text/javascript">
$(document).ready(function(){
    $('.addnewcontactfromorganization').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: '#oform',
      cssclass: 'overlay-contact-addnew',
      closeselector: '[name="oform.buttons.cancel"]',
      noform: function(el, pbo) {return 'reload';},
      config: {
          closeOnClick: false,
          closeOnEsc: false
      }
    });
});
</script>
"""


grok.templatedir('templates')


class Organization(BaseView):

    def update(self):
        super(Organization, self).update()
        self.organization = self.context
        organization = self.organization

        contactable = IContactable(organization)
        organizations = contactable.organizations
        self.parent_organizations = [org for org in organizations]
        self.parent_organizations.remove(organization)

        catalog = api.portal.get_tool('portal_catalog')
        context_path = '/'.join(organization.getPhysicalPath())
        self.sub_organizations = catalog.searchResults(portal_type="organization",
                                                       path={'query': context_path,
                                                             'depth': 1},
                                                       sort_on='getObjPositionInParent')
        self.positions = self.context.get_positions()
        sm = getSecurityManager()
        self.can_add = sm.checkPermission('Add portal content', self.context)
        self.addnew_script = ADDNEW_OVERLAY

    def display_date(self, date):
        """Display date nicely in template."""
        return self.context.toLocalizedTime(date_to_DateTime(date))


class SubOrganizations(BrowserView):

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')
        context_path = '/'.join(self.context.getPhysicalPath())
        self.sub_organizations = catalog.searchResults(portal_type="organization",
                                                       path={'query': context_path,
                                                             'depth': 1},
                                                       sort_on='getObjPositionInParent')
        return self.index()


class OtherContacts(grok.View):
    """Displays other contacts list"""
    grok.name('othercontacts')
    grok.context(IOrganization)

    held_positions = ''

    def update(self):
        organization = self.context
        othercontacts = []
        held_positions = organization.get_held_positions()
        held_positions.sort(key=lambda x: x.get_sortable_title())
        for hp in held_positions:
            contact = {}
            person = hp.get_person()
            contact['person'] = person
            contact['title'] = person.Title()
            contact['held_position'] = hp.Title()
            contact['label'] = hp.get_label()
            contact['obj'] = hp
            contact['display_photo'] = api.portal.get_registry_record(
                name='display_contact_photo_on_organization_view',
                interface=IContactCoreParameters)
            contact['has_photo'] = contact['display_photo'] and hp.photo or None

            if IContactDetails.providedBy(hp):
                contactable = hp
            elif IContactDetails.providedBy(person):
                contactable = person

            contact['email'] = contactable.email
            contact['phone'] = contactable.phone
            contact['cell_phone'] = contactable.cell_phone
            contact['fax'] = contactable.fax
            contact['im_handle'] = contactable.im_handle
            contact['website'] = get_valid_url(contactable.website)

            othercontacts.append(contact)

        self.othercontacts = othercontacts

from five import grok

from AccessControl import getSecurityManager

from plone import api

from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.interfaces import IContactable
from collective.contact.core.indexers import held_position_sortable_title
from collective.contact.core.behaviors import IContactDetails
from collective.contact.core.content.organization import IOrganization
from collective.contact.core.browser.utils import get_valid_url
from collective.contact.core.browser.utils import date_to_DateTime


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


class OtherContacts(grok.View):
    """Displays other contacts list"""
    grok.name('othercontacts')
    grok.context(IOrganization)

    held_positions = ''

    def update(self):
        organization = self.context
        othercontacts = []
        held_positions = organization.get_held_positions()
        held_positions.sort(key=lambda x: held_position_sortable_title(x)())
        for hp in held_positions:
            contact = {}
            person = hp.get_person()
            contact['title'] = person.Title()
            contact['held_position'] = hp.Title()
            contact['label'] = hp.label
            contact['obj'] = hp

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

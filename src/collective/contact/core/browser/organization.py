from AccessControl import getSecurityManager
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.browser.utils import get_ttw_fields
from collective.contact.core.interfaces import IContactable


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

class Organization(BaseView):

    name = ''
    type = ''
    parent_organizations = []
    sub_organizations = []
    positions = []

    def update(self):
        super(Organization, self).update()
        self.organization = self.context
        organization = self.organization

        self.name = organization.Title()
        factory = getUtility(IVocabularyFactory, "OrganizationTypesOrLevels")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(organization.organization_type).title

        contactable = IContactable(organization)
        organizations = contactable.organizations
        self.parent_organizations = [org for org in organizations]
        self.parent_organizations.remove(organization)
        self.organizations = organizations

        catalog = getToolByName(self.context, 'portal_catalog')
        context_path = '/'.join(organization.getPhysicalPath())
        self.sub_organizations = catalog.searchResults(portal_type="organization",
                                                       path={'query': context_path,
                                                             'depth': 1})
        self.positions = self.context.get_positions()

        contact_details = contactable.get_contact_details()
        self.email = contact_details['email']
        self.phone = contact_details['phone']
        self.cell_phone = contact_details['cell_phone']
        self.im_handle = contact_details['im_handle']
        self.address = contact_details['address']

        # also show fields that were added TTW
        self.ttw_fields = get_ttw_fields(organization)

        held_positions = organization.get_held_positions()
        self.othercontacts = [hp.get_person() for hp in held_positions]
        sm = getSecurityManager()
        self.can_add = sm.checkPermission('Add portal content', self.context)
        self.addnew_script = ADDNEW_OVERLAY

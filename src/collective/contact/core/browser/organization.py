from AccessControl import getSecurityManager

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

    def update(self):
        super(Organization, self).update()
        self.organization = self.context
        organization = self.organization

        contactable = IContactable(organization)
        organizations = contactable.organizations
        self.parent_organizations = [org for org in organizations]
        self.parent_organizations.remove(organization)

        catalog = getToolByName(self.context, 'portal_catalog')
        context_path = '/'.join(organization.getPhysicalPath())
        self.sub_organizations = catalog.searchResults(portal_type="organization",
                                                       path={'query': context_path,
                                                             'depth': 1})
        self.positions = self.context.get_positions()

        held_positions = organization.get_held_positions()
        self.othercontacts = [hp.get_person() for hp in held_positions]
        sm = getSecurityManager()
        self.can_add = sm.checkPermission('Add portal content', self.context)
        self.addnew_script = ADDNEW_OVERLAY


from AccessControl import getSecurityManager

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from collective.contact.core.browser.contactable import BaseView
from collective.contact.core.interfaces import IContactable


ADDNEW_OVERLAY = """
<script type="text/javascript">
$(document).ready(function(){
    $('.addnewcontactfromposition').prepOverlay({
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


class Position(BaseView):

    def update(self):
        super(Position, self).update()
        self.position = self.context
        position = self.position
        factory = getUtility(IVocabularyFactory, "PositionTypes")
        vocabulary = factory(self.context)
        self.type = vocabulary.getTerm(position.position_type).title

        contactable = IContactable(position)
        self.organizations = contactable.organizations

        sm = getSecurityManager()
        self.can_add = sm.checkPermission('Add portal content', self.context)
        self.addnew_script = ADDNEW_OVERLAY

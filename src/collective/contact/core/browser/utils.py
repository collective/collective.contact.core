from collective.contact.core import _tr as _
from collective.contact.core.behaviors import IBirthday
from collective.contact.core.behaviors import IContactDetails
from DateTime import DateTime
from imio.fpaudit.utils import fplog
from plone import api
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from plone.schemaeditor.utils import non_fieldset_fields
from plone.supermodel.interfaces import ISchemaPolicy
from zope import schema
from zope.component import getUtility


IGNORED_BEHAVIORS = [IContactDetails, IBasic, IBirthday]


def audit_access(contact, context):
    """Logs access to a contact"""
    if api.portal.get_registry_record("collective.contact.core.interfaces.IContactCoreParameters."
                                      "audit_contact_access", default=False):
        req = contact.REQUEST
        ctx = ""
        if context == "edit":
            ctx = _("contact_edit")
        else:
            if req["URL"].endswith("/view"):
                ctx = _('contact_view')
        if ctx:
            main_obj = req["PARENTS"][0]
            extra = u"UID={} PATH={} CTX_PATH={} CTX={}".format(contact.UID(), contact.absolute_url_path(),
                                                                main_obj.absolute_url_path(), ctx)
            fplog("contacts", "AUDIT", extra)


def date_to_DateTime(date):
    """Convert datetime.date to DateTime.DateTime format"""
    return DateTime(date.year, date.month, date.day).Date()


def get_ttw_fields(obj):
    """Returns names of the fields that were added to obj through the web"""
    fti = getUtility(IDexterityFTI, name=obj.portal_type)
    full_schema = fti.lookupSchema()
    all_fields = schema.getFieldsInOrder(full_schema)

    schema_policy = getUtility(ISchemaPolicy, name=fti.schema_policy)
    original_schema = schema_policy.bases(None, None)[0]
    original_fields = schema.getFieldsInOrder(original_schema)
    new_fields = [field[0] for field in all_fields
                  if field[0] not in dict(original_fields).keys()]

    for behavior_id in fti.behaviors:
        behavior = getUtility(IBehavior, behavior_id).interface
        if behavior in IGNORED_BEHAVIORS or not IFormFieldProvider.providedBy(behavior):
            continue

        try:
            default_fieldset_fields = non_fieldset_fields(behavior)
            behavior_name = behavior_id.split('.')[-1]
            # @TODO: get generic method to get widget id
            new_fields.extend(['%s.%s' % (behavior_name, field_name)
                               for field_name in default_fieldset_fields])
        except Exception:
            pass

    return new_fields


def get_valid_url(url):
    """Returns valid url (i.e. an url which starts with http or https)
    """
    if url and not url.startswith('http'):
        return u'http://{0}'.format(url)
    else:
        return url

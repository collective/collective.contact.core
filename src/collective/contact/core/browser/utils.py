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
from Products.CMFPlone.utils import base_hasattr
from zope import schema
from zope.component import getUtility

import re


IGNORED_BEHAVIORS = [IContactDetails, IBasic, IBirthday]


def get_object_from_request(request, portal=None, default=None):
    """Returns the object from the request.
    Not used here but can be useful"""
    if not portal:
        portal = api.portal.get()
    published = request.get('PUBLISHED', None)
    if base_hasattr(published, "getTagName"):
        context = published
    else:
        context = base_hasattr(published, 'context') and published.context or None
    if not context or context == portal:
        referer = portal.REQUEST['HTTP_REFERER'].replace(portal.absolute_url() + '/', '')
        # remove view and parameters
        referer = re.sub(r'/@@[^?]*$', '', re.sub(r'\?.*$', '', referer))
        try:
            context = portal.unrestrictedTraverse(referer)
        except (KeyError, AttributeError):
            return default
            # if not hasattr(context, 'portal_type'):
            #     return default
    return context


def get_object_from_referer(portal, referer, default=None):
    """Returns the object from the referer"""
    referer = referer.replace(portal.absolute_url() + '/', '')
    # remove view and parameters
    referer = re.sub(r'/@@[^?]*$', '', re.sub(r'/\+\+add\+\+\w+', '', re.sub(r'\?.*$', '', referer)))
    try:
        obj = portal.unrestrictedTraverse(referer)
        if not base_hasattr(obj, 'portal_type'):
            if base_hasattr(obj, 'context'):  # on a view like contactlist/view
                return obj.context
            if base_hasattr(obj, 'im_self'):  # on org selection on held_position edit
                return obj.im_self
        return obj
    except (KeyError, AttributeError):
        return default


def audit_access(contact, context):
    """Logs access to a contact"""
    if api.portal.get_registry_record("collective.contact.core.interfaces.IContactCoreParameters."
                                      "audit_contact_access", default=False):
        filtered_pt = api.portal.get_registry_record("collective.contact.core.interfaces.IContactCoreParameters."
                                                     "audit_contact_types", default=[])
        if filtered_pt and contact.portal_type not in filtered_pt:
            return
        portal = api.portal.get()
        portal_path_len = len(portal.absolute_url_path())
        req = contact.REQUEST
        case = ""
        # logger.info("{}, {}, {}| {}| {}| {}".format(contact, context, req["URL"], req["HTTP_REFERER"],
        # req["PARENTS"][0], req["PUBLISHED"]))
        if req["ACTUAL_URL"].endswith("@@autocomplete-search"):  # when org autocomplete search on held_position edit
            return
        if req["ACTUAL_URL"].endswith("@@masterselect-jsonvalue"):  # when editing person with admin
            return
        if context == "edit":
            main_obj = req["PARENTS"][0]
            case = _("contact_edit")
        else:
            if "ajax_load" in req:  # overlay
                main_obj = get_object_from_referer(portal, req["HTTP_REFERER"])
                case = _('contact_overlay')
            else:  # simple view
                main_obj = req["PARENTS"][0]
                case = _('contact_view')
        if case:
            extra = u"UID={} PATH={} CTX_PATH={} CASE={}".format(contact.UID(),
                                                                 contact.absolute_url_path()[portal_path_len:],
                                                                 main_obj.absolute_url_path()[portal_path_len:], case)
            fplog("contacts", contact.portal_type, extra)


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

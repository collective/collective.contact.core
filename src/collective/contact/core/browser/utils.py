from DateTime import DateTime
from zope.component import getUtility
from zope import schema

from plone.supermodel.interfaces import ISchemaPolicy
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehavior
from plone.schemaeditor.utils import non_fieldset_fields
from plone.dexterity.interfaces import IDexterityFTI
from plone.app.dexterity.behaviors.metadata import IBasic

from collective.contact.core.behaviors import IBirthday
from collective.contact.core.behaviors import IContactDetails


IGNORED_BEHAVIORS = [IContactDetails, IBasic, IBirthday]


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
        except:
            pass

    return new_fields


def get_valid_url(url):
    """Returns valid url (i.e. an url which starts with http or https)
    """
    if url and not url.startswith('http'):
        return "http://{}".format(url)
    else:
        return url

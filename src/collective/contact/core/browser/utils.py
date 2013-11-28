from DateTime import DateTime
from zope.component import getUtility
from zope import schema

from plone.dexterity.interfaces import IDexterityFTI
from plone.supermodel.interfaces import ISchemaPolicy
from plone.behavior.interfaces import IBehavior
from plone.autoform.interfaces import IFormFieldProvider

from collective.contact.core.behaviors import IContactDetails
from plone.schemaeditor.utils import non_fieldset_fields


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
        if behavior == IContactDetails or not IFormFieldProvider.providedBy(behavior):
            continue

        default_fieldset_fields = non_fieldset_fields(behavior)
        behavior_name = behavior_id.split('.')[-1]
        # @TODO: get generic method to get widget id
        new_fields.extend(['%s.%s' % (behavior_name, field_name)
                           for field_name in default_fieldset_fields])

    return new_fields

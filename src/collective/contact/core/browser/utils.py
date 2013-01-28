from DateTime import DateTime
from zope.component import getUtility
from zope import schema

from plone.dexterity.interfaces import IDexterityFTI
from plone.supermodel.interfaces import ISchemaPolicy


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
    new_fields = frozenset(dict(all_fields).keys()) - \
                 frozenset(dict(original_fields).keys())
    return new_fields

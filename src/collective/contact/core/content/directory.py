from collective.contact.core import _
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from five import grok
from plone.autoform.directives import widget
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface


def is_valid_identifier(identifier):
    idnormalizer = getUtility(IIDNormalizer)
    return idnormalizer.normalize(identifier) == identifier


class INameTokenTableRowSchema(Interface):
    """Schema for dict rows used in DataGridFields
    name is the 'real' name
    token is the token used in the vocabularies
    """

    name = schema.TextLine(title=_(u"Name"))
    token = schema.TextLine(title=_(u"Token"), constraint=is_valid_identifier)


class IDirectory(model.Schema):
    """Interface for Directory content type"""

    position_types = schema.List(
        title=_("Position types"),
        value_type=DictRow(title=_(u'Position'),
                           schema=INameTokenTableRowSchema)
        )
    widget('position_types', DataGridFieldFactory, allow_reorder=True)

    organization_types = schema.List(
        title=_("Organization types"),
        value_type=DictRow(title=_(u'Organization'),
                           schema=INameTokenTableRowSchema)
        )
    widget('organization_types', DataGridFieldFactory, allow_reorder=True)

    organization_levels = schema.List(
        title=_("Organization levels"),
        value_type=DictRow(title=_(u'Organization level'),
                           schema=INameTokenTableRowSchema)
        )
    widget('organization_levels', DataGridFieldFactory, allow_reorder=True)


class Directory(Container):
    """Directory content type"""
    implements(IDirectory)


class DirectorySchemaPolicy(grok.GlobalUtility,
                            DexteritySchemaPolicy):
    """Schema policy for Directory content type"""
    grok.name("schema_policy_directory")

    def bases(self, schemaName, tree):
        return (IDirectory, )

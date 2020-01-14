# -*- coding: utf-8 -*-
from collective.contact.core import _
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.autoform.directives import widget
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class INameTokenTableRowSchema(Interface):
    """Schema for dict rows used in DataGridFields
    name is the 'real' name
    token is the token used in the vocabularies
    """
    name = schema.TextLine(title=_(u"Name"))
    token = schema.TextLine(title=_(u"Token"))


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


@implementer(IDirectory)
class Directory(Container):
    """Directory content type"""


class DirectorySchemaPolicy(DexteritySchemaPolicy):
    """Schema policy for Directory content type"""

    def bases(self, schemaName, tree):
        return (IDirectory, )

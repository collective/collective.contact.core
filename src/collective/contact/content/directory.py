from zope.interface import Interface, implements
from zope import schema

from five import grok

from plone.autoform.directives import widget
from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.supermodel import model

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from . import _


class INameTokenTableRowSchema(Interface):
    name = schema.TextLine(title=_(u"Name"))
    token = schema.TextLine(title=_(u"Token"))


class IDirectory(model.Schema):

    position_types = schema.List(
        title=_("Position types"),
        value_type=DictRow(title=_(u'Position'),
                           schema=INameTokenTableRowSchema)
        )
    widget(position_types=DataGridFieldFactory)

    organization_types = schema.List(
        title=_("Organization types"),
        value_type=DictRow(title=_(u'Organization'),
                           schema=INameTokenTableRowSchema)
        )
    widget(organization_types=DataGridFieldFactory)

    organization_levels = schema.List(
        title=_("Organization levels"),
        value_type=DictRow(title=_(u'Organization level'),
                           schema=INameTokenTableRowSchema)
        )
    widget(organization_levels=DataGridFieldFactory)


class Directory(Container):
    """ """
    implements(IDirectory)


class DirectorySchemaPolicy(grok.GlobalUtility,
                            DexteritySchemaPolicy):
    """ """
    grok.name("schema_policy_directory")

    def bases(self, schemaName, tree):
        return (IDirectory, )

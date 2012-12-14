from zope import interface
from zope.interface import implements
from zope import schema

from plone.dexterity.content import Container
from plone.directives import form

from five import grok

from z3c.form.form import extends
from z3c.form import field

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from . import _


class INameTokenTableRowSchema(interface.Interface):
    name = schema.TextLine(title=_(u"Name"))
    token = schema.TextLine(title=_(u"Token"))


class IDirectory(form.Schema):

    position_types = schema.List(
        title=_("Position types"),
        value_type=DictRow(title=_(u'Position'),
                           schema=INameTokenTableRowSchema)
        )
    form.widget(position_types=DataGridFieldFactory)

    organization_types = schema.List(
        title=_("Organization types"),
        value_type=DictRow(title=_(u'Organization'),
                           schema=INameTokenTableRowSchema)
        )
    form.widget(organization_types=DataGridFieldFactory)

    organization_levels=schema.List(
        title=_("Organization levels"),
        value_type=DictRow(title=_(u'Organization level'),
                           schema=INameTokenTableRowSchema)
        )
    form.widget(organization_levels=DataGridFieldFactory)


class Directory(Container):
    """ """
    implements(IDirectory)

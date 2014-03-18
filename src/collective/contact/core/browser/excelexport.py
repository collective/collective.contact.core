from zope.component import adapts
from zope.interface import Interface

from plone.dexterity.interfaces import IDexterityFTI

from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
from collective.contact.widget.interfaces import IContactChoice
from collective.excelexport.exportables.base import BaseExportableFactory
from collective.excelexport.exportables.dexterityfields import get_ordered_fields
from plone import api
from zope.component._api import getMultiAdapter
from collective.excelexport.interfaces import IExportable


class ContactFieldRenderer(BaseFieldRenderer):
    adapts(IContactChoice, Interface, Interface)

    def render_value(self, obj):
        value = self.get_value(obj)
        return self.render_collection_entry(obj, value)

    def render_collection_entry(self, obj, value):
        return value and value.to_object and value.to_object.get_full_title() or u""


class HeldPositionPersonInfoExportableFactory(BaseExportableFactory):
    adapts(IDexterityFTI, Interface, Interface)
    portal_types = ('held_position',)
    weight = 10

    def get_exportables(self):
        position_fields = [f[0] for f in get_ordered_fields(self.fti)]
        person_fti = api.portal.get_tool('portal_types').person
        person_fields = [f for n, f in get_ordered_fields(person_fti)
                         if n not in position_fields]
        exportables = [getMultiAdapter((field, self.context, self.request),
                                        interface=IExportable)
                       for field in person_fields]
        return exportables
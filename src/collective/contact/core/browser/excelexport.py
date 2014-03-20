from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import Interface

from plone.dexterity.interfaces import IDexterityFTI
from plone import api

try:
    from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
    from collective.excelexport.exportables.base import BaseExportableFactory
    from collective.excelexport.exportables.dexterityfields import get_ordered_fields
    from collective.excelexport.interfaces import IExportable
    HAS_EXCELEXPORT = True
except ImportError:
    HAS_EXCELEXPORT = False

from collective.contact.widget.interfaces import IContactChoice
from collective.contact.core.content.held_position import IHeldPosition


if HAS_EXCELEXPORT:

    class ContactFieldRenderer(BaseFieldRenderer):
        adapts(IContactChoice, Interface, Interface)

        def render_value(self, obj):
            value = self.get_value(obj)
            return self.render_collection_entry(obj, value)

        def render_collection_entry(self, obj, value):
            rel_obj = value and value.to_object
            if not rel_obj:
                return u""
            if IHeldPosition.providedBy(rel_obj):
                return rel_obj.get_full_title() or u""
            else:
                return rel_obj.Title()


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
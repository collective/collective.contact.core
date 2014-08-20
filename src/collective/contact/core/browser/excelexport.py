from zope.component import adapts
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface
from zope.interface import implements

from plone.dexterity.interfaces import IDexterityFTI
from plone import api

try:
    from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
    from collective.excelexport.exportables.base import BaseExportableFactory
    from collective.excelexport.exportables.dexterityfields import get_ordered_fields
    from collective.excelexport.interfaces import IExportable
    from collective.excelexport.exportables.dexterityfields import IFieldValueGetter
    HAS_EXCELEXPORT = True
except ImportError:
    HAS_EXCELEXPORT = False

from collective.contact.widget.interfaces import IContactChoice, IContactContent
from collective.contact.core.content.held_position import IHeldPosition
from collective.contact.core.interfaces import IContactable
from collective.contact.core.behaviors import ADDRESS_FIELDS


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
            person_fields = [(n, f) for n, f in get_ordered_fields(person_fti)
                             if n not in position_fields]

            exportables = []
            for field_name, field in person_fields:
                try:
                    # check if there is a specific adapter for the field name
                    exportable = getMultiAdapter(
                                        (field, self.context, self.request),
                                        interface=IExportable,
                                        name=field_name)
                except ComponentLookupError:
                    # get the generic adapter for the field
                    exportable = getMultiAdapter(
                                        (field, self.context, self.request),
                                        interface=IExportable)

                exportables.append(exportable)

            return exportables

    class ContactValueGetter(object):
        adapts(IContactContent)
        implements(IFieldValueGetter)

        def __init__(self, context):
            self.context = context

        def get(self, field):
            if field.__name__ in ADDRESS_FIELDS:
                address = IContactable(self.context).get_contact_details(('address',))['address']
                return address.get(field.__name__, None)

            return getattr(self.context, field.__name__, None)

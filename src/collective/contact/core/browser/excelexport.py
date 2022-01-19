from collective.contact.core.behaviors import ADDRESS_FIELDS
from collective.contact.core.interfaces import IContactable
from collective.contact.core.interfaces import IHeldPosition
from collective.contact.widget.interfaces import IContactChoice
from collective.contact.widget.interfaces import IContactContent
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.interfaces import INamedImageField
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from zope.interface import implements
from zope.interface import Interface


try:
    from collective.excelexport.exportables.base import BaseExportableFactory
    from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
    from collective.excelexport.exportables.dexterityfields import FileFieldRenderer as baseFileFieldRenderer
    from collective.excelexport.exportables.dexterityfields import get_ordered_fields
    from collective.excelexport.exportables.dexterityfields import IFieldValueGetter
    from collective.excelexport.interfaces import IExportable
    HAS_EXCELEXPORT = True
except ImportError:
    HAS_EXCELEXPORT = False


if HAS_EXCELEXPORT:

    class ImageFieldRenderer(baseFileFieldRenderer):
        adapts(INamedImageField, Interface, Interface)

        def render_value(self, obj):
            value = self.get_value(obj)
            return (value and "{}/@@images/{}?{}".format(
                obj.absolute_url(),
                self.field.__name__,
                value.filename.encode("utf8")) or u""
            )

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
                return safe_unicode(rel_obj.get_full_title()) or u""
            else:
                return safe_unicode(rel_obj.Title())

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

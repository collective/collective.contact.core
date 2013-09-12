from zope.interface import alsoProvides
from zope.interface import Interface
from zope import schema
from Acquisition import aq_base

from z3c.form.widget import ComputedWidgetAttribute
from z3c.form.widget import FieldWidget
from plone.supermodel import model

from plone.supermodel.directives import fieldset
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.formwidget.datetime.z3cform import DateWidget
from plone.app.textfield import RichText
from plone.app.dexterity.browser.types import TypeSchemaContext

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from collective.contact.core import _
from collective.contact.core.interfaces import IContactable
from collective.contact.widget.schema import ContactChoice, ContactList
from collective.contact.widget.source import ContactSourceBinder


class InvalidEmailAddress(schema.ValidationError):
    """Exception for invalid address"""
    __doc__ = _(u"Invalid email address")


def validateEmail(value):
    """Simple email validator"""
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


def get_parent_address(adapter):
    """Gets the address of the first parent in hierarchy"""
    if adapter.context.portal_type == "directory":
        return u''
    elif type(aq_base(adapter.context)) == TypeSchemaContext:
        return u""

    return IContactable(adapter.context).get_parent_address()


class IGlobalPositioning(model.Schema):
    """GlobalPositioning behavior"""

    fieldset(
        'global_positioning',
        label=_(u'Global positioning'),
        fields=('latitude', 'longitude')
        )

    latitude = schema.Float(
            title=_('Latitude'),
            description=_('Latitude'),
            min=-90.0,
            max=90.0,
            required=False,
            )

    longitude = schema.Float(
            title=_('Longitude'),
            description=_('Longitude'),
            min=-90.0,
            max=90.0,
            required=False,
            )

alsoProvides(IGlobalPositioning, IFormFieldProvider)


class IContactDetails(model.Schema):
    """Contact details behavior"""

    fieldset(
        'contact_details',
        label=_(u'Contact details'),
        fields=('phone',
                'cell_phone',
                'email',
                'im_handle',
                )
        )
    fieldset(
        'address',
        label=_(u'Address'),
        fields=('use_parent_address',
                'parent_address',
                'number',
                'street',
                'additional_address_details',
                'zip_code',
                'city',
                'region',
                'country',
                )
        )

    email = schema.TextLine(
        title=_(u"Email"),
        constraint=validateEmail,
        required=False,
        )

    phone = schema.TextLine(
        title=_(u"Phone"),
        required=False,
        )

    cell_phone = schema.TextLine(
        title=_(u"Cell phone"),
        required=False,
        )

    im_handle = schema.TextLine(
        title=_('Instant messenger handle'),
        required=False,
        )

    use_parent_address = MasterSelectBoolField(
        title=_("Use the belonging entity address"),
        slave_fields=(
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'country',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'region',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'zip_code',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'city',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'number',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'street',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'additional_address_details',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },

            {'masterID': 'form-widgets-IContactDetails-use_parent_address-0',
             'name': 'parent_address',
             'action': 'hide',
             'hide_values': 0,
             'siblings': True,
            },
        ),
        default=True,
        required=False,
    )

    parent_address = RichText(
        default_mime_type='text/html',
        output_mime_type='text/html',
        required=False,
        )
    form.mode(parent_address='display')

    country = schema.TextLine(
        title=_('Country'),
        required=False,
        )

    zip_code = schema.TextLine(
        title=_('Zip Code'),
        required=False,
        )

    city = schema.TextLine(
        title=_('City'),
        required=False,
        )

    street = schema.TextLine(
        title=_('Street'),
        required=False,
        )

    number = schema.TextLine(
        title=_('Number'),
        required=False,
        )

    region = schema.TextLine(
            title=_('Region'),
            required=False,
            )

    additional_address_details = schema.TextLine(
            title=_('Additional address details'),
            required=False,
            )

alsoProvides(IContactDetails, IFormFieldProvider)


DefaultUseParentAddress = ComputedWidgetAttribute(
    get_parent_address,
    field=IContactDetails['use_parent_address'], view=Interface)


DefaultParentAddress = ComputedWidgetAttribute(
    get_parent_address,
    field=IContactDetails['parent_address'], view=Interface)



def DateFieldWidget(field, request):
    """IFieldWidget factory for DatetimeWidget."""
    widget = FieldWidget(field, DateWidget(request))
    widget.years_range = (-200, 1)
    return widget


class IBirthday(model.Schema):

    form.widget(birthday=DateFieldWidget)
    birthday = schema.Date(
        title=_("Birthday"),
        required=False,
        )

alsoProvides(IBirthday, IFormFieldProvider)


class IRelatedOrganizations(model.Schema):
    """A content on which we can attach organizations
    """

    fieldset(
        'related_organizations',
        label=_(u'Related organizations'),
        fields=('related_organizations',),
        )

    related_organizations = ContactList(
            value_type=ContactChoice(
                    description=_("Search and attach organizations related to this one"),
                    source=ContactSourceBinder(portal_type=("organization",)),),
            required=False,
            addlink=False,
    )


alsoProvides(IRelatedOrganizations, IFormFieldProvider)
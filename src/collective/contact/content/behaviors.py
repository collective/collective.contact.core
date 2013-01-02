from zope.interface import alsoProvides
from zope import schema

from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.autoform.interfaces import IFormFieldProvider

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from collective.contact.content import _


class InvalidEmailAddress(schema.ValidationError):
    __doc__ = _(u"Invalid email address")


def validateEmail(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class IGlobalPositioning(model.Schema):

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

    fieldset(
            'contact_details',
            label=_(u'Contact details'),
            fields=('email',
                    'phone',
                    'cell_phone',
                    'im_handle',
                    'country',
                    'zip_code',
                    'city',
                    'street',
                    'number',
                    'region',
                    'additional_address_details'
                    )
        )

    email = schema.TextLine(
            title=_(u"Email"),
            description=_(u"Email address"),
            constraint=validateEmail,
            required=False,
        )

    phone = schema.TextLine(
            title=_(u"Phone"),
            description=_(u"Phone number"),
            required=False,
        )

    cell_phone = schema.TextLine(
            title=_(u"Cell phone"),
            description=_(u"Cell phone number"),
            required=False,
        )

    im_handle = schema.TextLine(
            title=_('Instant messenger handle'),
            description=_('Instant messenger handle'),
            required=False,
        )

    country = schema.TextLine(
            title=_('Country'),
            description=_(u'Country'),
            required=False,
            )

    zip_code = schema.TextLine(
            title=_('Zip Code'),
            description=_(u'Zip Code'),
            required=False,
            )

    city = schema.TextLine(
            title=_('City'),
            description=_(u'City'),
            required=False,
            )

    street = schema.TextLine(
            title=_('Street'),
            description=_(u'Street'),
            required=False,
            )

    number = schema.TextLine(
            title=_('Number'),
            description=_(u'Number'),
            required=False,
            )

    region = schema.TextLine(
            title=_('Region'),
            description=_(u'Region'),
            required=False,
            )

    additional_address_details = schema.TextLine(
            title=_('Additional address details'),
            description=_(u'Additional address details'),
            required=False,
            )

alsoProvides(IContactDetails, IFormFieldProvider)

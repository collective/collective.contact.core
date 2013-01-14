from zope.interface import alsoProvides
from zope import schema

from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.app.textfield import RichText

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
                'use_address_below',
                'country',
                'zip_code',
                'city',
                'street',
                'number',
                'region',
                'additional_address_details',
                # not a real field !
                'address_below',
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

    use_address_below = MasterSelectBoolField(
        title=_("Use the address below"),
        description=_("Use the address below"),
        default=True,
        slave_fields=(
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'country',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'region',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'zip_code',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'city',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'number',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'street',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },
            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'additional_address_details',
             'action': 'show',
             'hide_values': 0,
             'siblings': True,
            },

            {'masterID': 'form-widgets-IContactDetails-use_address_below-0',
             'name': 'address_below',
             'action': 'hide',
             'hide_values': 0,
             'siblings': True,
            },
        ),
        required=False,
    )

    address_below = RichText(
        default_mime_type='text/html',
        output_mime_type='text/html',
        default=u"""
<div id="address">
3, rue Philibert Lucot<br/>
75013 Paris
</div>
""",  # TODO: use address of the object self.context/@@address ???
# TODO: Hide this field and "use address below" field in view mode ?
        required=False,
        )
    form.mode(address_below='display')

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

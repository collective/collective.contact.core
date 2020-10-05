# -*- coding: utf8 -*-

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model

from plone.testing import z2
from collective.contact.widget.schema import ContactChoice
from collective.contact.widget.schema import ContactList
from collective.contact.widget.source import ContactSourceBinder
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import collective.contact.core


static_prefilter_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'', title=u'No filter'),
        SimpleTerm(value=u'{"portal_type":"person"}', title=u'Only people'),
        SimpleTerm(value=u'{"portal_type":"organization"}', title=u'Only organizations'),
    ]
)


def prefilter_default_value(context):
    return u'{"portal_type":"organization"}'


class IPrefiltering(model.Schema):

    contact_list_no_default = ContactList(
        title=u'Contact list (no default)',
        required=True,
        value_type=ContactChoice(
            source=ContactSourceBinder(
                portal_type=("organization", 'held_position', 'person', 'contact_list'),
            )
        ),
        prefilter_vocabulary=static_prefilter_vocabulary,
    )

    contact_list_with_contextual_default = ContactList(
        title=u'Contact list (with contextual default)',
        required=True,
        value_type=ContactChoice(
            source=ContactSourceBinder(
                portal_type=("organization", 'held_position', 'person', 'contact_list'),
            )
        ),
        prefilter_vocabulary=static_prefilter_vocabulary,
        prefilter_default_value=prefilter_default_value,
    )


alsoProvides(IPrefiltering, IFormFieldProvider)


class ContactContentLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.contact.core:testing')
        # insert some test data
        self.applyProfile(portal, 'collective.contact.core:test_data')
        setRoles(portal, TEST_USER_ID, ['Manager'])


COLLECTIVE_CONTACT_CORE = ContactContentLayer(
    zcml_package=collective.contact.core,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.contact.core:testing',
    name="COLLECTIVE_CONTACT_CORE")

INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_CONTACT_CORE, ),
    name="INTEGRATION")

FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CORE, ),
    name="FUNCTIONAL")

ACCEPTANCE = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CORE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ACCEPTANCE")

# -*- coding: utf8 -*-

from DateTime import DateTime

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing.helpers import login, setRoles
from plone.app.testing.interfaces import TEST_USER_NAME, TEST_USER_ID

from ecreall.helpers.testing import member as memberhelpers

import collective.contact.content


class ContactContentLayer(PloneWithPackageLayer):

    def insert_test_data(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        position_types = [{'Name': 'General', 'Token': 'general'},
                          {'Name': 'Sergeant', 'Token': 'sergeant'},
                          {'Name': 'Colonel', 'Token': 'colonel'},
                          {'Name': 'Lieutenant', 'Token': 'lieutenant'},
                          {'Name': 'Captain', 'Token': 'captain'},
                          {'Name': 'Admiral', 'Token': 'admiral'},
                          ]

        organization_types = [{'Name': 'Navy', 'Token': 'navy'},
                              {'Name': 'Army', 'Token': 'army'},
                              {'Name': 'Air force', 'Token': 'air_force'},
                              ]

        organization_levels = [{'Name': 'Corps', 'Token': 'corps'},
                               {'Name': 'Division', 'Token': 'division'},
                               {'Name': 'Brigade', 'Token': 'brigade'},
                               {'Name': 'Regiment', 'Token': 'regiment'},
                               {'Name': 'Squad', 'Token': 'squad'},
                               ]

        params = {'title': "Military directory",
                  'position_types': position_types,
                  'organization_types': organization_types,
                  'organization_levels': organization_levels,
                  }
        portal.invokeFactory('directory', 'mydirectory', **params)
        mydirectory = portal['mydirectory']

        params = {'lastname': 'De Gaulle',
                  'firstname': 'Charles',
                  'gender': 'M',
                  'person_title': u'Général',
                  'birthday': DateTime('1890-11-22'),
                  'email': 'charles.de.gaulle@armees.fr',
                  }
        mydirectory.invokeFactory('person', 'degaulle', **params)
        degaulle = mydirectory['degaulle']

        params = {'title': u"Armée de terre",
                  'organization_type': 'army',
                  }
        mydirectory.invokeFactory('organization', 'armeedeterre', **params)
        armeedeterre = mydirectory['armeedeterre']

        params = {'title': "Corps A",
                  'organization_type': 'corps',
                  }
        armeedeterre.invokeFactory('organization', 'corpsa', **params)
        corpsa = armeedeterre['corpsa']

        params = {'title': "Corps B",
                  'organization_type': 'corps',
                  }
        armeedeterre.invokeFactory('organization', 'corpsb', **params)

        params = {'title': "Division Alpha",
                  'organization_type': 'division',
                  }
        corpsa.invokeFactory('organization', 'divisionalpha', **params)

        params = {'title': u"General of armée de terre",
                  'position_type': 'general',
                  }
        armeedeterre.invokeFactory('position', 'general_adt', **params)

        params = {'start_date': DateTime('1940-05-25'),
                  'end_date': DateTime('1970-11-09'),
                  'position': armeedeterre,
                  }
        degaulle.invokeFactory('held_position', 'adt', **params)

        general_adt = armeedeterre['general_adt']
        params = {'start_date': DateTime('1940-05-25'),
                  'end_date': DateTime('1970-11-09'),
                  'position': general_adt,
                  }
        degaulle.invokeFactory('held_position', 'gadt', **params)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.contact.content:testing')
        self.insert_test_data(portal)


COLLECTIVE_CONTACT_CONTENT = ContactContentLayer(
    zcml_package=collective.contact.content,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.contact.content:testing',
    name="COLLECTIVE_CONTACT_CONTENT")

INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_CONTACT_CONTENT, ),
    name="INTEGRATION")

FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_CONTACT_CONTENT, ),
    name="FUNCTIONAL")

# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
#
# GNU General Public License (GPL)
#

__docformat__ = 'plaintext'

import datetime

from zope import component
from zope.intid.interfaces import IIntIds

from z3c.relationfield.relation import RelationValue

import logging
logger = logging.getLogger('collective.contact.content: setuphandlers')


def isNotCollectiveContactContentProfile(context):
    return context.readDataFile("collective_contact_content_marker.txt") is None


def isNotTestDataProfile(context):
    return context.readDataFile("collective_contact_content_test_data_marker.txt") is None


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotCollectiveContactContentProfile(context): return
    # we CAN NOT reinstall the product using portal_quickinstaller because
    # it removes manualy added fields for dexterity types
    import traceback
    for line in traceback.format_stack():
        if 'QuickInstallerTool.py' in line and 'reinstallProducts' in line:
            raise Exception, 'You can not reinstall this product, use portal_setup to re-apply the relevant profile !'
    # we need to remove the default model_source added to our portal_types
    # XXX to be done


def createTestData(context):
    """Create test data for collective.contact.content"""
    if isNotTestDataProfile(context): return
    portal = context.getSite()

    position_types = [{'name': 'General', 'token': 'general'},
                      {'name': 'Sergeant', 'token': 'sergeant'},
                      {'name': 'Colonel', 'token': 'colonel'},
                      {'name': 'Lieutenant', 'token': 'lieutenant'},
                      {'name': 'Captain', 'token': 'captain'},
                      {'name': 'Admiral', 'token': 'admiral'},
                      ]

    organization_types = [{'name': 'Navy', 'token': 'navy'},
                          {'name': 'Army', 'token': 'army'},
                          {'name': 'Air force', 'token': 'air_force'},
                          ]

    organization_levels = [{'name': 'Corps', 'token': 'corps'},
                           {'name': 'Division', 'token': 'division'},
                           {'name': 'Brigade', 'token': 'brigade'},
                           {'name': 'Regiment', 'token': 'regiment'},
                           {'name': 'Squad', 'token': 'squad'},
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
              'person_title': 'Général',
              'birthday': datetime.date(1890, 11, 22),
              'email': 'charles.de.gaulle@armees.fr',
              }
    mydirectory.invokeFactory('person', 'degaulle', **params)
    degaulle = mydirectory['degaulle']

    params = {'title': "Armée de terre",
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

    params = {'title': "General of armée de terre",
              'position_type': 'general',
              }
    armeedeterre.invokeFactory('position', 'general_adt', **params)

    intids = component.getUtility(IIntIds)

    params = {'start_date': datetime.date(1940, 5, 25),
              'end_date': datetime.date(1970, 11, 9),
              'position': RelationValue(intids.getId(armeedeterre)),
              }
    degaulle.invokeFactory('held_position', 'adt', **params)

    general_adt = armeedeterre['general_adt']
    params = {'start_date': datetime.date(1940, 5, 25),
              'end_date': datetime.date(1970, 11, 9),
              'position': RelationValue(intids.getId(general_adt)),
              }
    degaulle.invokeFactory('held_position', 'gadt', **params)

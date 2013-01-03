# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
#
# GNU General Public License (GPL)
#

__docformat__ = 'plaintext'

from DateTime import DateTime

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

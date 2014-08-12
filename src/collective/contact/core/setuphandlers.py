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
logger = logging.getLogger('collective.contact.core: setuphandlers')


def isNotCollectiveContactContentProfile(context):
    return context.readDataFile("collective_contact_core_marker.txt") is None


def isNotTestDataProfile(context):
    return context.readDataFile("collective_contact_core_test_data_marker.txt") is None


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotCollectiveContactContentProfile(context):
        return
    # we CAN NOT reinstall the product using portal_quickinstaller because
    # it removes manualy added fields for dexterity types
    import traceback
    for line in traceback.format_stack():
        if 'QuickInstallerTool.py' in line and 'reinstallProducts' in line:
            raise Exception('You can not reinstall this product, use portal_setup to re-apply the relevant profile !')
    # we need to remove the default model_source added to our portal_types
    # XXX to be done


def create_test_contact_data(portal):
    """Create test contact data in portal"""
    position_types = [{'name': u'General', 'token': u'general'},
                      {'name': u'Sergeant', 'token': u'sergeant'},
                      {'name': u'Colonel', 'token': u'colonel'},
                      {'name': u'Lieutenant', 'token': u'lieutenant'},
                      {'name': u'Captain', 'token': u'captain'},
                      {'name': u'Admiral', 'token': u'admiral'},
                      ]

    organization_types = [{'name': u'Navy', 'token': u'navy'},
                          {'name': u'Army', 'token': u'army'},
                          {'name': u'Air force', 'token': u'air_force'},
                          ]

    organization_levels = [{'name': u'Corps', 'token': u'corps'},
                           {'name': u'Division', 'token': u'division'},
                           {'name': u'Regiment', 'token': u'regiment'},
                           {'name': u'Squad', 'token': u'squad'},
                           ]

    params = {'title': u"Military directory",
              'position_types': position_types,
              'organization_types': organization_types,
              'organization_levels': organization_levels,
              }
    portal.invokeFactory('directory', 'mydirectory', **params)
    mydirectory = portal['mydirectory']

    params = {'lastname': u'De Gaulle',
              'firstname': u'Charles',
              'gender': u'M',
              'person_title': u'Général',
              'birthday': datetime.date(1901, 11, 22),
              'email': u'charles.de.gaulle@armees.fr',
              'country': u'France',
              'city': u"Colombey les deux églises",
              'number': u'6bis',
              'street': u'rue Jean Moulin',
              'zip_code': u'52330',
              'additional_address_details': u'bâtiment D',
              'use_parent_address': False,
              'website': 'www.charles-de-gaulle.org'
              }
    mydirectory.invokeFactory('person', 'degaulle', **params)
    degaulle = mydirectory['degaulle']

    params = {'lastname': u'Pepper',
              'gender': u'M',
              'person_title': u'Sergent',
              'birthday': datetime.date(1967, 6, 1),
              'email': u'sgt.pepper@armees.fr',
              'phone': u'0288552211',
              'city': u'Liverpool',
              'country': u'England',
              'use_parent_address': False,
              'website': 'http://www.sergent-pepper.org'
              }
    mydirectory.invokeFactory('person', 'pepper', **params)
    pepper = mydirectory['pepper']

    params = {'lastname': u'Rambo',
              'firstname': u'John',
              'phone': u'0788556644',
              'use_parent_address': True,
              }
    mydirectory.invokeFactory('person', 'rambo', **params)

    params = {'lastname': u'Draper',
              'firstname': u'John',
              'person_title': u'Mister',
              'use_parent_address': True,
              }
    mydirectory.invokeFactory('person', 'draper', **params)
    draper = mydirectory['draper']

    params = {'title': u"Armée de terre",
              'organization_type': u'army',
              'use_parent_address': True,
              }
    mydirectory.invokeFactory('organization', 'armeedeterre', **params)
    armeedeterre = mydirectory['armeedeterre']

    params = {'title': u"Corps A",
              'organization_type': u'corps',
              'street': u"rue Philibert Lucot",
              'city': u'Orléans',
              'country': u'France',
              'use_parent_address': False,
              }
    armeedeterre.invokeFactory('organization', 'corpsa', **params)
    corpsa = armeedeterre['corpsa']

    params = {'title': u"Corps B",
              'organization_type': u'corps',
              'use_parent_address': True,
              }
    armeedeterre.invokeFactory('organization', 'corpsb', **params)

    params = {'title': u"Division Alpha",
              'organization_type': u'division',
              'use_parent_address': True,
              }
    corpsa.invokeFactory('organization', 'divisionalpha', **params)

    params = {'title': u"Division Beta",
              'organization_type': u'division',
              'use_parent_address': True,
              }
    corpsa.invokeFactory('organization', 'divisionbeta', **params)

    divisionalpha = corpsa['divisionalpha']

    params = {'title': u"Régiment H",
              'organization_type': u'regiment',
              'number': u"11",
              'street': u"rue de l'harmonie",
              'city': u"Villeneuve d'Ascq",
              'zip_code': u'59650',
              'country': u'France',
              'use_parent_address': False,
              }
    divisionalpha.invokeFactory('organization', 'regimenth', **params)

    regimenth = divisionalpha['regimenth']
    params = {'title': u"Brigade LH",
              'organization_type': u'squad',
              'use_parent_address': True,
              }
    regimenth.invokeFactory('organization', 'brigadelh', **params)
    brigadelh = regimenth['brigadelh']

    params = {'title': u"Général de l'armée de terre",
              'position_type': u'general',
              'use_parent_address': True,
              }
    armeedeterre.invokeFactory('position', 'general_adt', **params)

    params = {'title': u"Capitaine de la division Alpha",
              'position_type': u'captain',
              'use_parent_address': True,
              }
    divisionalpha.invokeFactory('position', 'capitaine_alpha', **params)
    capitaine_alpha = divisionalpha['capitaine_alpha']

    params = {'title': u"Sergent de la brigade LH",
              'position_type': u'sergeant',
              'cell_phone': u'0654875233',
              'email': u'brigade_lh@armees.fr',
              'im_handle': u'brigade_lh@jabber.org',
              'use_parent_address': True,
              }
    brigadelh.invokeFactory('position', 'sergent_lh', **params)
    sergent_lh = brigadelh['sergent_lh']

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
              'label': u"Émissaire OTAN"
              }
    degaulle.invokeFactory('held_position', 'gadt', **params)

    params = {'start_date': datetime.date(1980, 6, 5),
              'position': RelationValue(intids.getId(sergent_lh)),
              }
    pepper.invokeFactory('held_position', 'sergent_pepper', **params)

    params = {'position': RelationValue(intids.getId(capitaine_alpha)),
              }
    draper.invokeFactory('held_position', 'captain_crunch', **params)


def createTestData(context):
    """Create test data for collective.contact.core"""
    if isNotTestDataProfile(context):
        return
    portal = context.getSite()
    create_test_contact_data(portal)

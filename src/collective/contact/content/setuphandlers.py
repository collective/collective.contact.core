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
              }
    mydirectory.invokeFactory('person', 'pepper', **params)
    pepper = mydirectory['pepper']

    params = {'lastname': u'Rambo',
              'firstname': u'John',
              'phone': u'0788556644',
              }
    mydirectory.invokeFactory('person', 'rambo', **params)

    params = {'title': u"Armée de terre",
              'organization_type': u'army',
              }
    mydirectory.invokeFactory('organization', 'armeedeterre', **params)
    armeedeterre = mydirectory['armeedeterre']

    params = {'title': u"Corps A",
              'organization_type': u'corps',
              'street': u"rue Philibert Lucot",
              'city': u'Orléans',
              'country': u'France',
              }
    armeedeterre.invokeFactory('organization', 'corpsa', **params)
    corpsa = armeedeterre['corpsa']

    params = {'title': u"Corps B",
              'organization_type': u'corps',
              }
    armeedeterre.invokeFactory('organization', 'corpsb', **params)

    params = {'title': u"Division Alpha",
              'organization_type': u'division',
              }
    corpsa.invokeFactory('organization', 'divisionalpha', **params)

    params = {'title': u"Division Beta",
              'organization_type': u'division',
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
              }
    divisionalpha.invokeFactory('organization', 'regimenth', **params)

    regimenth = divisionalpha['regimenth']
    params = {'title': u"Brigade LH",
              'organization_type': u'squad',
              }
    regimenth.invokeFactory('organization', 'brigadelh', **params)
    brigadelh = regimenth['brigadelh']

    params = {'title': u"Général de l'armée de terre",
              'position_type': u'general',
              }
    armeedeterre.invokeFactory('position', 'general_adt', **params)

    params = {'title': u"Sergent de la brigade LH",
              'position_type': u'sergent',
              'cell_phone': u'0654875233',
              'email': u'brigade_lh@armees.fr',
              'im_handle': u'brigade_lh@jabber.org',
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
              }
    degaulle.invokeFactory('held_position', 'gadt', **params)

    params = {'start_date': datetime.date(1980, 6, 5),
              'end_date': datetime.date(1988, 1, 19),
              'position': RelationValue(intids.getId(sergent_lh)),
              }
    pepper.invokeFactory('held_position', 'sergent_pepper', **params)

# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
#
# GNU General Public License (GPL)
#

__docformat__ = "plaintext"

from collective.contact.core.interfaces import IContactCoreParameters
from plone import api
from z3c.relationfield.relation import RelationValue
from zope import component
from zope.intid.interfaces import IIntIds

import datetime
import logging


# from plone.registry.interfaces import IRegistry

logger = logging.getLogger("collective.contact.core: setuphandlers")


def isNotCollectiveContactContentProfile(context):
    return context.readDataFile("collective_contact_core_marker.txt") is None


def isNotTestDataProfile(context):
    return context.readDataFile("collective_contact_core_test_data_marker.txt") is None


def postInstall(context):
    """Called as at the end of the setup process."""
    # the right place for your custom code
    if isNotCollectiveContactContentProfile(context):
        return
    # Set default values in registry
    for name in (
        "person_contact_details_private",
        "person_title_in_title",
        "use_held_positions_to_search_person",
        "use_description_to_search_person",
    ):
        val = api.portal.get_registry_record(name=name, interface=IContactCoreParameters)
        if val is None:
            api.portal.set_registry_record(name=name, value=True, interface=IContactCoreParameters)
    # we need to remove the default model_source added to our portal_types
    # XXX to be done


def create_test_contact_data(portal):
    """Create test contact data in portal"""
    position_types = [
        {"name": "General", "token": "general"},
        {"name": "Sergeant", "token": "sergeant"},
        {"name": "Colonel", "token": "colonel"},
        {"name": "Lieutenant", "token": "lieutenant"},
        {"name": "Captain", "token": "captain"},
        {"name": "Admiral", "token": "admiral"},
    ]

    organization_types = [
        {"name": "Navy", "token": "navy"},
        {"name": "Army", "token": "army"},
        {"name": "Air force", "token": "air_force"},
    ]

    organization_levels = [
        {"name": "Corps", "token": "corps"},
        {"name": "Division", "token": "division"},
        {"name": "Regiment", "token": "regiment"},
        {"name": "Squad", "token": "squad"},
    ]
    # Examples structure
    # ------------------
    # organizations (* = organization, £ = position)
    #     * Armée de terre
    #         * Corps A
    #             * Division Alpha
    #                 * Régiment H
    #                     * Brigade LH
    #                         £ Sergent
    #                 £ Capitaine
    #             * Division Beta
    #         * Corps B
    #         £ Général
    #
    # persons (> = person, @ = held_position)
    #     > De Gaulle
    #         @ Armée de terre
    #         @ Général
    #     > Pepper
    #         @ Sergent
    #     > Rambo
    #         @ Brigade LH
    #     > Draper
    #         @ Capitaine
    #         @ Division Beta

    params = {
        "title": "Military directory",
        "position_types": position_types,
        "organization_types": organization_types,
        "organization_levels": organization_levels,
    }
    portal.invokeFactory("directory", "mydirectory", **params)
    mydirectory = portal["mydirectory"]

    params = {
        "lastname": "De Gaulle",
        "firstname": "Charles",
        "gender": "M",
        "person_title": "Général",
        "birthday": datetime.date(1901, 11, 22),
        "email": "charles.de.gaulle@private.com",
        "country": "France",
        "city": "Colombey les deux églises",
        "number": "6bis",
        "street": "rue Jean Moulin",
        "zip_code": "52330",
        "additional_address_details": "bâtiment D",
        "use_parent_address": False,
        "website": "www.charles-de-gaulle.org",
    }
    mydirectory.invokeFactory("person", "degaulle", **params)
    degaulle = mydirectory["degaulle"]

    params = {
        "lastname": "Pepper",
        "gender": "M",
        "person_title": "Mister",
        "birthday": datetime.date(1967, 6, 1),
        "email": "stephen.pepper@private.com",
        "phone": "0288443344",
        "city": "Liverpool",
        "country": "England",
        "use_parent_address": False,
        "website": "http://www.stephen-pepper.org",
    }
    mydirectory.invokeFactory("person", "pepper", **params)
    pepper = mydirectory["pepper"]

    params = {
        "lastname": "Rambo",
        "firstname": "John",
        "phone": "0788556644",
        "use_parent_address": True,
    }
    mydirectory.invokeFactory("person", "rambo", **params)
    rambo = mydirectory["rambo"]

    params = {
        "lastname": "Draper",
        "firstname": "John",
        "person_title": "Mister",
        "use_parent_address": False,
    }

    mydirectory.invokeFactory("person", "draper", **params)
    draper = mydirectory["draper"]

    params = {
        "title": "Armée de terre",
        "organization_type": "army",
        "phone": "01000000001",
        "email": "contact@armees.fr",
        "use_parent_address": False,
        "city": "Paris",
        "street": "Avenue des Champs-Élysées",
        "number": "1",
        "zip_code": "75008",
        "country": "France",
        "enterprise_number": "BE123456789",
    }
    mydirectory.invokeFactory("organization", "armeedeterre", **params)
    armeedeterre = mydirectory["armeedeterre"]

    params = {
        "title": "Corps A",
        "organization_type": "corps",
        "street": "rue Philibert Lucot",
        "city": "Orléans",
        "country": "France",
        "use_parent_address": False,
    }
    armeedeterre.invokeFactory("organization", "corpsa", **params)
    corpsa = armeedeterre["corpsa"]

    params = {
        "title": "Corps B",
        "organization_type": "corps",
        "use_parent_address": True,
    }
    armeedeterre.invokeFactory("organization", "corpsb", **params)

    params = {
        "title": "Division Alpha",
        "organization_type": "division",
        "use_parent_address": True,
    }
    corpsa.invokeFactory("organization", "divisionalpha", **params)

    params = {
        "title": "Division Beta",
        "organization_type": "division",
        "use_parent_address": True,
    }
    corpsa.invokeFactory("organization", "divisionbeta", **params)

    divisionalpha = corpsa["divisionalpha"]
    divisionbeta = corpsa["divisionbeta"]

    params = {
        "title": "Régiment H",
        "organization_type": "regiment",
        "number": "11",
        "street": "rue de l'harmonie",
        "city": "Villeneuve d'Ascq",
        "zip_code": "59650",
        "country": "France",
        "use_parent_address": False,
    }
    divisionalpha.invokeFactory("organization", "regimenth", **params)

    regimenth = divisionalpha["regimenth"]
    params = {
        "title": "Brigade LH",
        "organization_type": "squad",
        "use_parent_address": True,
    }
    regimenth.invokeFactory("organization", "brigadelh", **params)
    brigadelh = regimenth["brigadelh"]

    params = {
        "title": "Général de l'armée de terre",
        "position_type": "general",
        "email": "general@armees.fr",
        "use_parent_address": False,
        "city": "Lille",
        "street": "Rue de la Porte d'Ypres",
        "number": "1",
        "zip_code": "59800",
        "country": "France",
    }
    armeedeterre.invokeFactory("position", "general_adt", **params)

    params = {
        "title": "Capitaine de la division Alpha",
        "position_type": "captain",
        "use_parent_address": True,
    }
    divisionalpha.invokeFactory("position", "capitaine_alpha", **params)
    capitaine_alpha = divisionalpha["capitaine_alpha"]

    params = {
        "title": "Sergent de la brigade LH",
        "position_type": "sergeant",
        "cell_phone": "0654875233",
        "email": "brigade_lh@armees.fr",
        "im_handle": "brigade_lh@jabber.org",
        "use_parent_address": True,
    }
    brigadelh.invokeFactory("position", "sergent_lh", **params)
    sergent_lh = brigadelh["sergent_lh"]

    intids = component.getUtility(IIntIds)

    params = {
        "start_date": datetime.date(1940, 5, 25),
        "end_date": datetime.date(1970, 11, 9),
        "position": RelationValue(intids.getId(armeedeterre)),
    }
    degaulle.invokeFactory("held_position", "adt", **params)

    general_adt = armeedeterre["general_adt"]
    params = {
        "start_date": datetime.date(1940, 5, 25),
        "end_date": datetime.date(1970, 11, 9),
        "position": RelationValue(intids.getId(general_adt)),
        "label": "Émissaire OTAN",
        "phone": "0987654321",
        "country": "France",
        "use_parent_address": True,
    }
    degaulle.invokeFactory("held_position", "gadt", **params)

    params = {
        "start_date": datetime.date(1980, 6, 5),
        "position": RelationValue(intids.getId(sergent_lh)),
        "email": "sgt.pepper@armees.fr",
        "phone": "0288552211",
        "city": "Liverpool",
        "street": "Water Street",
        "number": "1",
        "zip_code": "L3 4FP",
        "country": "England",
        "use_parent_address": False,
        "website": "http://www.sergent-pepper.org",
    }
    pepper.invokeFactory("held_position", "sergent_pepper", **params)

    params = {
        "position": RelationValue(intids.getId(capitaine_alpha)),
        "use_parent_address": True,
    }
    draper.invokeFactory("held_position", "captain_crunch", **params)

    params = {
        "position": RelationValue(intids.getId(divisionbeta)),
        "use_parent_address": True,
    }
    draper.invokeFactory("held_position", "divisionbeta", **params)

    params = {
        "position": RelationValue(intids.getId(brigadelh)),
        "use_parent_address": True,
    }
    rambo.invokeFactory("held_position", "brigadelh", **params)


def createTestData(context):
    """Create test data for collective.contact.core"""
    if isNotTestDataProfile(context):
        return
    portal = context.getSite()
    create_test_contact_data(portal)

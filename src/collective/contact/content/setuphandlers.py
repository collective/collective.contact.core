# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
#
# GNU General Public License (GPL)
#

__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('collective.contact.content: setuphandlers')

def isNotCollectiveContactContentProfile(context):
    return context.readDataFile("collective_contact_content_marker.txt") is None

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotCollectiveContactContentProfile(context): return
    logStep("postInstall", context)
    site = context.getSite()
    # we CAN NOT reinstall the product using portal_quickinstaller because
    # it removes manualy added fields for dexterity types
    #import ipdb; ipdb.set_trace()
    # we need to be sure 
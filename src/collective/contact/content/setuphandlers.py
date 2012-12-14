# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2012 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier Bastien <gbastien@commune.sambreville.be>, Stephan Geulette
<stephan.geulette@uvcw.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('MeetingCommunes: setuphandlers')
from Products.MeetingCommunes.config import PROJECTNAME
from Products.MeetingCommunes.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.PloneMeeting.config import TOPIC_TYPE, TOPIC_SEARCH_SCRIPT, TOPIC_TAL_EXPRESSION
from Products.PloneMeeting.exportimport.content import ToolInitializer
##/code-section HEAD

def isNotMeetingCommunesProfile(context):
    return context.readDataFile("MeetingCommunes_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingCommunesProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingCommunesProfile(context): return
    logStep("postInstall", context)
    site = context.getSite()
    #need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    reinstallPloneMeeting(context, site)
    addPowerObserversGroup(context, site)
    adaptFCKMenuStyles(context, site)
    showHomeTab(context, site)
    recreateMeetingConfigsPortalTabs(context, site)
    reinstallPloneMeetingSkin(context, site)



##code-section FOOT
def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'"%(method, '/'.join(context._profile_path.split(os.sep)[-3:])))

def isMeetingCommunesConfigureProfile(context):
    return context.readDataFile("MeetingCommunes_examples_fr_marker.txt") or \
           context.readDataFile("MeetingCommunes_examples_marker.txt") or \
           context.readDataFile("MeetingCommunes_cpas_marker.txt") or \
           context.readDataFile("MeetingCommunes_tests_marker.txt")

def isMeetingCommunesMigrationProfile(context):
    return context.readDataFile("MeetingCommunes_migrations_marker.txt")

def installMeetingCommunes(context):
    """ Run the default profile"""
    if not isMeetingCommunesConfigureProfile(context):
        return
    logStep("installMeetingCommunes", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingCommunes:default')

def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not isMeetingCommunesConfigureProfile(context): return

    logStep("initializeTool", context)
    #PloneMeeting is no more a dependency to avoid
    #magic between quickinstaller and portal_setup
    #so install it manually
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()

def _addTopics(context, site):
    '''
       Add searches to the added meetingConfigs
       Proposed items, validated items and decided items
    '''

    logStep("_addTopics", context)
    topicsInfo = (
    # Items in state 'proposed'
    ( 'searchproposeditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('proposed', ), "python: not here.portal_plonemeeting.userIsAmong('reviewers')", '',
    ),
    # Items that need to be validated
    ( 'searchitemstovalidate',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('proposed', ), "python: here.portal_plonemeeting.userIsAmong('reviewers')", 'searchItemsToValidate',
    ),
    # Items in state 'validated'
    ( 'searchvalidateditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('validated', ), '', '',
    ),
    # All 'decided' items
    ( 'searchdecideditems',
    (  ('Type', 'ATPortalTypeCriterion', 'MeetingItem'),
    ), ('accepted', 'refused', 'delayed', 'accepted_but_modified',), '', '',
    ),
    )

    #Add these searches by meeting config
    for meetingConfig in site.portal_plonemeeting.objectValues("MeetingConfig"):
        for topicId, topicCriteria, stateValues, topicCondition, topicScript in topicsInfo:
            #if reinstalling, we need to check if the topic does not already exist
            if hasattr(meetingConfig.topics, topicId):
                continue
            meetingConfig.topics.invokeFactory('Topic', topicId)
            topic = getattr(meetingConfig.topics, topicId)
            topic.setExcludeFromNav(True)
            topic.setTitle(topicId)
            for criterionName, criterionType, criterionValue in topicCriteria:
                criterion = topic.addCriterion(field=criterionName,
                                                criterion_type=criterionType)
                topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
                criterionValue = '%s%s' % (criterionValue, meetingConfig.getShortName())
                criterion.setValue([criterionValue])
            topic.manage_addProperty(TOPIC_TAL_EXPRESSION, topicCondition, 'string')
            topic.manage_addProperty(TOPIC_SEARCH_SCRIPT, topicScript, 'string')

            stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
            stateCriterion.setValue(stateValues)
            topic.setLimitNumber(True)
            topic.setItemCount(20)
            topic.setSortCriterion('created', True)
            topic.setCustomView(True)
            topic.setCustomViewFields(['Title', 'CreationDate', 'Creator', 'review_state'])
            topic.reindexObject()

def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingCommunesProfile(context): return

    logStep("reinstallPloneMeeting", context)    
    _installPloneMeeting(context)

def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)

def addPowerObserversGroup(context, site):
    """
      Add a Plone group configured to receive MeetingPowerObservers
      These users can see the items and meetings since they are frozen
    """
    if isNotMeetingCommunesProfile(context): return
    logStep("addPowerObserversGroup", context)
    groupId = "meetingpowerobservers"
    if not groupId in site.portal_groups.listGroupIds():
        site.portal_groups.addGroup(groupId, title=site.utranslate("powerObserversGroupTitle", domain='PloneMeeting'))
        site.portal_groups.setRolesForGroup(groupId, ('MeetingObserverGlobal','MeetingPowerObserver'))

def adaptFCKMenuStyles(context, site):
    """
       Add the "highlight-red" style to the FCK menu styles
    """
    if isNotMeetingCommunesProfile(context): return

    logStep("adaptFCKMenuStyles", context)

    fckeditor_properties = getattr(site.portal_properties, 'fckeditor_properties', None)

    if fckeditor_properties:
        fck_menu_styles = fckeditor_properties.fck_menu_styles
        if not "highlight-red" in fck_menu_styles:
            # Add the style
            newStyle = """
<Style name="Mettre en évidence" element="span">
<Attribute name="class" value="highlight-red" />
</Style>"""
            fck_menu_styles=fck_menu_styles+newStyle
            fckeditor_properties.manage_changeProperties(fck_menu_styles=fck_menu_styles)

def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingCommunesProfile(context): return

    logStep("showHomeTab", context)
    
    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")

def recreateMeetingConfigsPortalTabs(context, site):
    """
       portal_tabs for a MeetingConfig are created during
       PloneMeeting MeetingConfigs creation (at install time).
       This is "logged" by portal_quickinstaller and when reinstalling,
       these tabs are removed...
       Instead of using actions.xml, we recreate them for every existing
       MeetingConfigs so it works with every profiles (example_fr, zcpas, ...)
    """
    if isNotMeetingCommunesProfile(context): return

    logStep("recreateMeetingConfigsPortalTabs", context)
    
    cfgs = site.portal_plonemeeting.objectValues('MeetingConfig')
    for cfg in cfgs:
        cfg.createTab()

def reinstallPloneMeetingSkin(context, site):
    """
       Reinstall Products.plonemeetingskin as the reinstallation of MeetingCommunes
       change the portal_skins layers order
    """
    if isNotMeetingCommunesProfile(context) and not isMeetingCommunesConfigureProfile: return

    logStep("reinstallPloneMeetingSkin", context)
    try:
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the Products.plonemeetingskin profile is not available
        # (not using plonemeetingskin or in tests?) we pass...
        pass

def finalizeExampleInstance(context):
    """
       Some parameters can not be handled by the PloneMeeting installation,
       so we handle this here
    """
    if not isMeetingCommunesConfigureProfile(context): return

    site = context.getSite()

    logStep("finalizeExampleInstance", context)
    # add the test user 'bourgmestre' to the PowerObservers group
    member = site.portal_membership.getMemberById('bourgmestre')
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), 'meetingpowerobservers')

    # add some topics
    _addTopics(context, site)

    # define some parameters for 'meeting-config-college'
    # items are sendable to the 'meeting-config-council'
    mc_college = getattr(site.portal_plonemeeting, 'meeting-config-college')
    mc_college.setMeetingConfigsToCloneTo(['meeting-config-council', ])
    # add some topcis to the portlet_todo
    mc_college.setToDoListTopics([getattr(mc_college.topics, 'searchdecideditems'),
                          getattr(mc_college.topics, 'searchitemstovalidate'),
                          getattr(mc_college.topics, 'searchallitemsincopy'),
                          getattr(mc_college.topics, 'searchallitemstoadvice'),
                         ])
    # call updateCloneToOtherMCActions inter alia
    mc_college.at_post_edit_script()

    # define some parameters for 'meeting-config-council'
    mc_council = getattr(site.portal_plonemeeting, 'meeting-config-council')
    # add some topcis to the portlet_todo
    mc_council.setToDoListTopics([getattr(mc_council.topics, 'searchdecideditems'),
                          getattr(mc_council.topics, 'searchitemstovalidate'),
                          getattr(mc_council.topics, 'searchallitemsincopy'),
                         ])
    #finally, re-launch plonemeetingskin and MeetingCommunes skins step
    # because PM has been installed before the import_data profile and messed up skins layers
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin', 'skins')

    

# ------------------------------------------------------------------------------
# ---------------------- MIGRATIONS SCRIPTS ------------------------------------
# ------------------------------------------------------------------------------

def unregisterSomeSteps(context):
    """
      Some old steps are no more used, remove them!
    """
    if not isMeetingCommunesMigrationProfile(context): return

    logStep("unregisterSomeSteps", context)

    site = context.getSite()
    stepsToRemove = ['addSearches-MeetingCommunes', 'MeetingCommunes-addPowerObserversGroup', ]
    for stepToRemove in stepsToRemove:
        try:
            site.portal_setup._import_registry.unregisterStep(stepToRemove)
        except KeyError:
            #the step does not exist (already removed)
            pass

def adaptItemsToValidateTopic(context):
    """
      Old versions of the searchitemstovalidate topic did not use a search script, correct this!
    """
    if not isMeetingCommunesMigrationProfile(context): return

    logStep("adaptItemsToValidateTopic", context)

    site = context.getSite()
    for mc in site.portal_plonemeeting.objectValues('MeetingConfig'):
        topic = getattr(mc.topics, 'searchitemstovalidate', None)
        if topic:
            if not topic.hasProperty(TOPIC_SEARCH_SCRIPT):
                topic.manage_addProperty(TOPIC_SEARCH_SCRIPT, 'searchItemsToValidate', 'string')
            else:
                topic.manage_changeProperties(topic_search_script='searchItemsToValidate')

##/code-section FOOT

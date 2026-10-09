*** Settings ***
Documentation  Plone 6 Classic UI keywords. Same keyword names and arguments as ui_plone4.robot.
...            Robot Framework 3.2 syntax: shared with the Plone 4.3 (Python 2) environment.
...            Modals: pat-plone-modal; contact widget: livesearch (collective.contact.widget python3).
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=.modal-dialog
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist
# profiles/default/registry/icons.xml
&{TYPE_ICONS}  directory=journals.svg  held_position=person-badge.svg  organization=diagram-3-fill.svg
...            person=file-earmark-person-fill.svg  position=briefcase.svg


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Click button  css=#buttons-login
    Wait until page contains element  css=#personaltools-menulink

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions ul
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories > a
    Wait until element is visible  css=#plone-contentmenu-factories ul

Add new
    [Documentation]  Add form of a content type, from the add menu of the current page
    [Arguments]  ${portal_type}
    Open the add menu
    Click link  css=#plone-contentmenu-factories a#${portal_type}
    Wait until page contains element  css=#form

Click the portal tab
    [Documentation]  Item of the global navigation, by content id
    [Arguments]  ${content_id}
    Click link  css=#portal-globalnav li.${content_id} a

Click the edit tab
    Click link  css=#contentview-edit a
    Wait until page contains element  css=#form

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id}  href  ${url}

The personal action is not available
    [Arguments]  ${action_id}
    Page should not contain element  css=#personaltools-${action_id}

The modal is open
    [Documentation]  Overlay (Plone 4) or modal (Plone 6) showing a form
    Wait until element is visible  ${MODAL} form

Modal element
    [Documentation]  Locator of the element with this id inside the modal
    ...              (an argument starting with # would be a robot comment)
    [Arguments]  ${id}
    [Return]  ${MODAL} [id="${id}"]

Save the modal
    Click button  css=.modal-footer #form-buttons-save

Cancel the modal
    Click button  css=.modal-footer #form-buttons-cancel

Click the modal button
    [Documentation]  Button of the form shown in the modal, by name (e.g. oform.buttons.save):
    ...              pat-plone-modal shows the form buttons in the modal footer
    [Arguments]  ${name}
    Click button  css=.modal-footer [name="${name}"]

The modal is closed
    Wait until page does not contain element  ${MODAL}

The status message contains
    [Arguments]  ${text}
    Wait until element contains  css=.portalMessage  ${text}

Confirm the deletion
    [Documentation]  Delete button of the delete_confirmation page
    Click button  css=#form-buttons-Delete

The page is not an error
    Page should not contain  ${ERROR_PAGE_TEXT}

The page is not found
    Page should contain  ${NOT_FOUND_TEXT}

The edit link is not available
    Page should not contain element  css=#contentview-edit

Type icon file
    [Documentation]  File name of the icon of a content type (plone.icon.contenttype/* registry records)
    [Arguments]  ${portal_type}
    [Return]  ${TYPE_ICONS}[${portal_type}]

Select in the contact widget
    [Documentation]  Search a contact widget (by widget id) and select the first result containing the text
    [Arguments]  ${widget_id}  ${text}
    Input text  css=#${widget_id}-widgets-query  ${text}
    ${result}=  Set variable  xpath=(//*[@id="${widget_id}-autocomplete"]//li[contains(@class, "search-result")][contains(., "${text}")])[1]
    Wait until element is visible  ${result}
    Click element  ${result}

The contact widget results contain
    [Arguments]  ${widget_id}  ${text}
    Wait until element is visible  xpath=//*[@id="${widget_id}-autocomplete"]//li[contains(@class, "search-result")][contains(., "${text}")]

The contact widget results do not contain
    [Arguments]  ${widget_id}  ${text}
    Page should not contain element  xpath=//*[@id="${widget_id}-autocomplete"]//li[contains(@class, "search-result")][contains(., "${text}")]

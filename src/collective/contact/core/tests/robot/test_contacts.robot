*** Settings ***
#Test Setup        Open test browser
#Test Teardown     Close all browsers

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers

*** Keywords ***
Go to directory
    Go to  ${PLONE_URL}/mydirectory

Close Overlay
    Click Element  css=div.overlay div.close

Overlay should close
    Element should not remain visible  id=exposeMask
    Wait until keyword succeeds  60  1  Page should not contain element  css=div.overlay

Overlay is opened
    Wait Until Page Contains Element  css=.overlay


*** Test cases ***
Directory is available
    Log in as site owner
    Click link  css=#portaltab-mydirectory a
    Element should contain  css=#content h1  Military directory

Create a new organization
    Log in as site owner
    Go to directory
    Open Add New Menu
    Click link  css=#plone-contentmenu-factories a#organization
    Wait Until Page Contains Element  css=#form-widgets-IBasic-title
    Input Text  css=#form-widgets-IBasic-title  Squadron five
    Click Button    Save
    Page should contain  Squadron five
    Go to directory
    Element should contain  organizations  Squadron five

Can create new contact from organization
    Log in as site owner
    Go to  ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha
    Page should contain link  css=.addnewcontactfromorganization
    Click link  css=.addnewcontactfromorganization
    Overlay is opened
    Wait For Condition  return $('.overlay h1').text() === "Create Contact"
    Element should contain  oform-widgets-organization-input-fields  Armée de terre / Corps A / Division Alpha
    Input text  oform-widgets-person-widgets-query  Ramb
    Click element  oform-widgets-person-widgets-query
    Wait Until Page Contains Element  css=.ac_results
    Click element  css=.ac_results li:nth-child(1)
    Click button  Add

Can create new contact from position
    Log in as site owner
    Go to  ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh/sergent_lh
    Page should contain link  css=.addnewcontactfromposition
    Click link  css=.addnewcontactfromposition
    Overlay is opened
    Wait For Condition  return $('.overlay h1').text() === "Create Contact"
    Element should contain  oform-widgets-organization-input-fields  Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH
    Element should contain  oform-widgets-position-input-fields  Sergent de la brigade LH, Brigade LH (Armée de terre)
    Input text  oform-widgets-person-widgets-query  Ramb
    Click element  oform-widgets-person-widgets-query
    Wait Until Page Contains Element  css=.ac_results
    Click element  css=.ac_results li:nth-child(1)
    Click button  Add

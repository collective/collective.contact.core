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

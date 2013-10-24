*** Settings ***

Resource  Selenium2Screenshots/keywords.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Test Setup  Run keywords  Open SauceLabs test browser  Remove military directory
Test Teardown  Run keywords  Report test status  Close all browsers

*** Keywords ***

Remove military directory
    Log in as site owner
    Remove Content  mydirectory

a Site Owner
    Log in as site owner

a French Plone site
    Go to  ${PLONE_URL}/@@language-controlpanel
    Select From List  form.default_language  fr
    Click Button  form.actions.save

Add new
    [Arguments]   ${name}
    Open Add New Menu
    Click link  css=#plone-contentmenu-factories a#${name}
    Wait Until Page Contains Element  css=#form-widgets-IBasic-title


*** Test cases ***
Create new directory
    Given a Site Owner
    And a French Plone site
    Go to  ${PLONE_URL}
    Add new  directory
    Input Text  css=#form-widgets-IBasic-title  Annuaire

    Input Text  form-widgets-position_types-AA-widgets-name  Directeur
    Click element  css=#formfield-form-widgets-position_types .insert-row
    Input Text  form-widgets-position_types-AA-widgets-name  Responsable d'équipe
    Click element  css=#formfield-form-widgets-position_types .insert-row
    Input Text  form-widgets-position_types-AA-widgets-name  Commercial
    Click element  form-widgets-organization_types-AA-widgets-name

    Input Text  form-widgets-organization_types-AA-widgets-name  Association
    Click element  css=#formfield-form-widgets-organization_types .insert-row
    Input Text  form-widgets-organization_types-AA-widgets-name  Entreprise
    Click element  css=#formfield-form-widgets-organization_types .insert-row

    Input Text  form-widgets-organization_levels-AA-widgets-name  Département
    Click element  css=#formfield-form-widgets-organization_levels .insert-row
    Input Text  form-widgets-organization_levels-AA-widgets-name  Service
    Click element  css=#formfield-form-widgets-organization_levels .insert-row
    Input Text  form-widgets-organization_levels-AA-widgets-name  Équipe
    Click element  css=#formfield-form-widgets-organization_levels .insert-row

    Capture and crop page screenshot  add_directory.png  portal-column-content

    Click Button    form-buttons-save
    Page should contain  Annuaire

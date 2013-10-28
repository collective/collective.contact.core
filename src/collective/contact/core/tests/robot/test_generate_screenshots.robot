*** Settings ***

Resource  Selenium2Screenshots/keywords.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  keywords.robot

Test Setup  Run keywords  Open SauceLabs test browser  Remove military directory
Test Teardown  Run keywords  Report test status  Close all browsers


*** Variables ***

${SSDIR}  /tmp/images


*** Keywords ***

Remove military directory
    Log in as site owner
    Remove Content  mydirectory

Go to directory
    Go to  ${PLONE_URL}/annuaire

I create a new directory
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

    Capture and crop page screenshot  ${SSDIR}/add_directory.png  portal-column-content
    Click Button    form-buttons-save
    Page should contain  Annuaire

I add a person
    [Arguments]   ${firstname}  ${lastname}  ${gender}  ${ss_name}
    Go to directory
    Add new  person
    Input Text  form-widgets-firstname  ${firstname}
    Input Text  form-widgets-lastname  ${lastname}
    Run Keyword If  '${gender}' == 'M'  Click element  form-widgets-gender-0
    Run Keyword If  '${gender}' == 'F'  Click element  form-widgets-gender-1
    Input text  form-widgets-IBirthday-birthday-day  11
    Input text  form-widgets-IBirthday-birthday-year  1978
    Capture and crop page screenshot  ${SSDIR}/${ss_name}.png  portal-column-content
    Click Button    form-buttons-save

I add Doremi company
    Go to directory
    Add new  organization
    Input Text  form-widgets-IBasic-title  Dorémi
    Input Text  form-widgets-IBasic-description  Société de services en logiciels libres
    Select From List  form-widgets-organization_type  Entreprise
    Capture and crop page screenshot  ${SSDIR}/add_organization.png  portal-column-content

    # add contact info
    Click link  fieldsetlegend-0
    Input Text  form-widgets-IContactDetails-phone  0311223344
    Input Text  form-widgets-IContactDetails-fax  0322334455
    Input Text  form-widgets-IContactDetails-website  http://www.doremi.fr
    Capture and crop page screenshot  ${SSDIR}/contact_info_form.png  portal-column-content

    # add address
    Click link  fieldsetlegend-1
    Input Text  form-widgets-IContactDetails-number  2
    Input Text  form-widgets-IContactDetails-street  avenue de Paris
    Input Text  form-widgets-IContactDetails-zip_code  59000
    Input Text  form-widgets-IContactDetails-city  Lille
    Input Text  form-widgets-IContactDetails-country  France
    Capture and crop page screenshot  ${SSDIR}/address_form.png  portal-column-content

    Click Button    form-buttons-save
    Page should contain  Dorémi
    Go to directory
    Element should contain  organizations  Dorémi

I add CEO position
    Go to  ${PLONE_URL}/annuaire/doremi
    Add new  position
    Input Text  form-widgets-IBasic-title  Président directeur général
    Capture and crop page screenshot  ${SSDIR}/add_position.png  portal-column-content
    Click link  fieldsetlegend-1
    Capture and crop page screenshot  ${SSDIR}/position_parent_address.png  formfield-form-widgets-IContactDetails-use_parent_address  formfield-form-widgets-IContactDetails-parent_address
    Unselect Checkbox  form-widgets-IContactDetails-use_parent_address-0
    Wait until keyword succeeds  60  1  Element should not be visible  formfield-form-widgets-IContactDetails-parent_address
    Input Text  form-widgets-IContactDetails-number  165
    Input Text  form-widgets-IContactDetails-street  rue de Lille
    Input Text  form-widgets-IContactDetails-zip_code  75010
    Input Text  form-widgets-IContactDetails-city  Paris
    Input Text  form-widgets-IContactDetails-country  France
    Capture and crop page screenshot  ${SSDIR}/position_own_address.png  fieldset-1
    Click Button    form-buttons-save

I add a team
    [Arguments]   ${name}  ${ss_name}
    Go to  ${PLONE_URL}/annuaire/doremi
    Add new  organization
    Input Text  form-widgets-IBasic-title  ${name}
    Select From List  form-widgets-organization_type  Équipe
    Capture and crop page screenshot  ${SSDIR}/${ss_name}.png  portal-column-content
    ### Click link  fieldsetlegend-1
    ### Unselect Checkbox  form-widgets-IContactDetails-use_parent_address-0
    ### Select Checkbox  form-widgets-IContactDetails-use_parent_address-0
    ### Wait until page contains  avenue de Paris
    ### Capture and crop page screenshot  ${SSDIR}/team_parent_address.png  fieldset-1
    Click Button  form-buttons-save

Capture download vcard link
    Go to  ${PLONE_URL}/annuaire/m-jean-legrand/president-directeur-general-doremi
    Update element style  css=div#download_vcard a  outline  1px solid red
    Capture and crop page screenshot  ${SSDIR}/download_vcard_link.png  portal-column-content

I add a CEO contact
    Go to  ${PLONE_URL}/annuaire/doremi/president-directeur-general
    Update element style  css=.addnewcontactfromposition  outline  1px solid red
    Capture and crop page screenshot  ${SSDIR}/add_contact_link.png  portal-column-content
    Click link  css=.addnewcontactfromposition
    Overlay is opened
    Wait until keyword succeeds  60  1  Element should contain  oform-widgets-organization-input-fields  Dorémi
    Wait until keyword succeeds  60  1  Element should contain  oform-widgets-position-input-fields  Président directeur général

    Capture and crop page screenshot  ${SSDIR}/contact_overlay_before.png  css=.overlay

    # capture tooltip : doesn't work anymore ?
    Click link  css=#oform-widgets-organization-autocomplete .link-tooltip
    Wait Until Page Contains Element  css=.tooltip
    Capture and crop page screenshot  ${SSDIR}/tooltip_orga.png  css=.tooltip

    Click element  oform-widgets-person-widgets-query
    Input text  oform-widgets-person-widgets-query  Dura
    Click element  oform-widgets-person-widgets-query
    Wait Until Page Contains Element  css=.ac_results
    Capture and crop page screenshot  ${SSDIR}/person_autocomplete.png  formfield-oform-widgets-person  css=.ac_results
    Click link  css=#oform-widgets-person-autocomplete .addnew
    Overlay is opened
    Wait Until Page Contains Element  form-widgets-firstname
    Input Text  form-widgets-firstname  Jean
    Input Text  form-widgets-lastname  Legrand
    Click element  form-widgets-gender-0
    Input text  form-widgets-IBirthday-birthday-day  8
    Input text  form-widgets-IBirthday-birthday-year  1972
    Capture and crop page screenshot  ${SSDIR}/add_person_in_overlay.png  css=.overlay
    Click Button    form-buttons-save  # person overlay
    Person overlay should close
    Wait until keyword succeeds  60  1  Element should contain  oform-widgets-person-input-fields  Jean Legrand
    Capture and crop page screenshot  ${SSDIR}/contact_overlay_after.png  css=.overlay
    Click button  oform-buttons-save  # contact overlay
    Overlay should close


*** Test cases ***

Generate screenshots
    Given a Site Owner
    And a French Plone site
    I create a new directory
    I add a person  Pierre  Durand  M  pdurand
    I add a person  Marie  Durand  F  mdurand
    I add a person  Pierre  Dupont  M  pdupont
    I add Doremi company
    I add CEO position
    I add a CEO contact
    Capture download vcard link

    I add a team  Marketing et commercial  team_marketing
    I add a team  Développement  team_dev
    #Add contact directly in this team
    Go to  ${PLONE_URL}/annuaire/doremi
    Capture and crop page screenshot  ${SSDIR}/orga_page.png  portal-column-content

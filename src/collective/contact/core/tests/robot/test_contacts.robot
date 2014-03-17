*** Settings ***

#Test Setup        Open test browser
#Test Teardown     Close all browsers

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  keywords.robot

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
    Add new  organization
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
    Wait until keyword succeeds    60    1    Element should be visible    oform-widgets-organization-input-fields
    Element should contain  oform-widgets-organization-input-fields  Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH
    Wait until keyword succeeds    60    1    Element should be visible    oform-widgets-position-input-fields
    Element should contain  oform-widgets-position-input-fields  Sergent de la brigade LH, Brigade LH (Armée de terre)
    Input text  oform-widgets-person-widgets-query  Ramb
    Click element  oform-widgets-person-widgets-query
    Wait Until Page Contains Element  css=.ac_results
    Click element  css=.ac_results li:nth-child(1)
    Click button  Add


Show parent address if it exists in creation
    Log in as site owner
    Go to  ${PLONE_URL}/mydirectory/armeedeterre/corpsa
    Add new  organization
    Click link  Address
    Checkbox Should Be Selected  form-widgets-IContactDetails-use_parent_address-0
    Element should contain  address  rue Philibert Lucot
    Element should contain  address  Orléans
    Element should contain  address  France
    Element should not be visible  formfield-form-widgets-IContactDetails-number
    Element should not be visible  formfield-form-widgets-IContactDetails-street
    Element should not be visible  formfield-form-widgets-IContactDetails-city
    Element should not be visible  formfield-form-widgets-IContactDetails-country


Show parent address if it exists in edition
    Log in as site owner
    Go to  ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha/capitaine_alpha
    Click Edit In Edit Bar
    Click link  Address
    ${original_speed} =  Get Selenium speed
    Set Selenium speed  1
    Checkbox Should Be Selected  form-widgets-IContactDetails-use_parent_address-0
    Element should contain  address  rue Philibert Lucot
    Set Selenium speed  ${original_speed}
    Element should contain  address  Orléans
    Element should contain  address  France
    Element should not be visible  formfield-form-widgets-IContactDetails-number
    Element should not be visible  formfield-form-widgets-IContactDetails-street
    Element should not be visible  formfield-form-widgets-IContactDetails-city
    Element should not be visible  formfield-form-widgets-IContactDetails-country


Don't show use parent address checkbox if no parent address in creation
    Log in as site owner
    Go to  ${PLONE_URL}/mydirectory/armeedeterre/corpsb
    Add new  position
    Click link  Address
    Page should contain element  formfield-form-widgets-IContactDetails-number
    Page should contain element  formfield-form-widgets-IContactDetails-street
    Page should contain element  formfield-form-widgets-IContactDetails-city
    Page should contain element  formfield-form-widgets-IContactDetails-country
    Element should not be visible  form-widgets-IContactDetails-use_parent_address-0


Don't show use parent address checkbox if no parent address in edition
    Log in as site owner
    Go to  ${PLONE_URL}/mydirectory/armeedeterre/corpsb
    Click Edit In Edit Bar
    Click link  Address
    Page should contain element  formfield-form-widgets-IContactDetails-number
    Page should contain element  formfield-form-widgets-IContactDetails-street
    Page should contain element  formfield-form-widgets-IContactDetails-city
    Page should contain element  formfield-form-widgets-IContactDetails-country
    Element should not be visible  form-widgets-IContactDetails-use_parent_address-0

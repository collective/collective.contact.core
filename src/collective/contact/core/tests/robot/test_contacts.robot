*** Settings ***
Test Setup        Open SauceLabs test browser
Test Teardown     Run keywords    Report test status    Close all browsers
Resource          plone/app/robotframework/keywords.robot    #Test Setup    Open test browser    #Test Teardown    Close all browsers
Resource          plone/app/robotframework/saucelabs.robot
Resource          keywords.robot

*** Test cases ***
Directory is available
    [Tags]    Go
    Log in as site owner and wait
    Click link    css=#portaltab-mydirectory a
    Element should contain    css=#content h1    Military directory

Create a new organization
    [Tags]    Go
    Log in as site owner and wait
    Go to directory
    Add new    organization
    Input Text    css=#form-widgets-IBasic-title    Squadron five
    Click Button    Save
    Page should contain    Squadron five
    Go to directory
    Element should contain    organizations    Squadron five

Can create new contact from organization
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha
    Page should contain link    css=.addnewcontactfromorganization
    Click link    css=.addnewcontactfromorganization
    Overlay is opened
    Wait For Condition    return $('.overlay h1').text() === "Create Contact"
    Element should contain    oform-widgets-organization-input-fields    Armée de terre / Corps A / Division Alpha
    Sleep  1
    Input text    oform-widgets-person-widgets-query    Ramb
    Click element    oform-widgets-person-widgets-query
    Wait Until Page Contains Element    css=.ac_results
    Click element    css=.ac_results li:nth-child(1)
    Click button    Add

Can create new person from organization
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha
    Click link    css=.addnewcontactfromorganization
    Wait For Condition    return $('.overlay h1').text() === "Create Contact"
    Element should not be visible    css=#formfield-oform-widgets-person .addnew-block
    Sleep  1
    Input text    oform-widgets-person-widgets-query    Chuck Norris
    Element should become visible    css=#formfield-oform-widgets-person .addnew-block
    Click link    Create Person
    Wait Until Page Contains    Add Person
    ${original_speed} =    Get Selenium speed
    Set Selenium speed    1
    Textfield Value Should Be    form-widgets-lastname    Norris
    Set Selenium speed    ${original_speed}
    Textfield Value Should Be    form-widgets-firstname    Chuck
    Click element    form-widgets-gender-0
    Click button    Save
    Wait Until Page Contains    Chuck Norris
    Click button    Add
    Wait Until Page Contains Element    other-contacts
    Element Should Contain    other-contacts    Chuck Norris

Can create new contact from position
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh/sergent_lh
    Page should contain link    css=.addnewcontactfromposition
    Click link    css=.addnewcontactfromposition
    Overlay is opened
    Wait For Condition    return $('.overlay h1').text() === "Create Contact"
    Element should not be visible    css=#oform-widgets-position-input-fields
    Element should contain    oform-widgets-organization-input-fields    Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH
    Input text    oform-widgets-person-widgets-query    Ramb
    Click element    oform-widgets-person-widgets-query
    Wait Until Page Contains Element    css=.ac_results
    Click element    css=.ac_results li:nth-child(1)
    Sleep  1
    Element should become visible    css=#oform-widgets-position-input-fields
    Element should contain    oform-widgets-position-input-fields    Sergent de la brigade LH, Brigade LH (Armée de terre)
    Click button    Add

Show parent address if it exists in creation
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsa
    Add new    organization
    Click link    Address
    Checkbox Should Be Selected    form-widgets-IContactDetails-use_parent_address-0
    Element should contain    css=.address    rue Philibert Lucot
    Element should contain    css=.address    Orléans
    Element should contain    css=.address    France
    Element should not be visible    formfield-form-widgets-IContactDetails-number
    Element should not be visible    formfield-form-widgets-IContactDetails-street
    Element should not be visible    formfield-form-widgets-IContactDetails-city
    Element should not be visible    formfield-form-widgets-IContactDetails-country

Show parent address if it exists in edition
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha/capitaine_alpha
    Click Edit In Edit Bar
    Click link    Address
    ${original_speed} =    Get Selenium speed
    Set Selenium speed    1
    Checkbox Should Be Selected    form-widgets-IContactDetails-use_parent_address-0
    Element should contain    css=.address    rue Philibert Lucot
    Set Selenium speed    ${original_speed}
    Element should contain    css=.address    Orléans
    Element should contain    css=.address    France
    Element should not be visible    formfield-form-widgets-IContactDetails-number
    Element should not be visible    formfield-form-widgets-IContactDetails-street
    Element should not be visible    formfield-form-widgets-IContactDetails-city
    Element should not be visible    formfield-form-widgets-IContactDetails-country

Show use parent address checkbox if no parent address when creating a position
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsb
    Add new    position
    Click link    Address
    Page should contain element    formfield-form-widgets-IContactDetails-number
    Page should contain element    formfield-form-widgets-IContactDetails-street
    Page should contain element    formfield-form-widgets-IContactDetails-city
    Page should contain element    formfield-form-widgets-IContactDetails-country
    Element should be visible    form-widgets-IContactDetails-use_parent_address-0

Don't show use parent address checkbox in edition if no parent address and use parent address is False
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsa
    Click Edit In Edit Bar
    Click link    Address
    Page should contain element    formfield-form-widgets-IContactDetails-number
    Page should contain element    formfield-form-widgets-IContactDetails-street
    Page should contain element    formfield-form-widgets-IContactDetails-city
    Page should contain element    formfield-form-widgets-IContactDetails-country
    Element should not be visible    form-widgets-IContactDetails-use_parent_address-0

Show use parent address checkbox in edition if no parent address and use parent address is True
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/armeedeterre/corpsb
    Click Edit In Edit Bar
    Click link    Address
    Page should contain element    formfield-form-widgets-IContactDetails-number
    Page should contain element    formfield-form-widgets-IContactDetails-street
    Page should contain element    formfield-form-widgets-IContactDetails-city
    Page should contain element    formfield-form-widgets-IContactDetails-country
    Element should be visible    form-widgets-IContactDetails-use_parent_address-0

*** Keywords ***
Go to directory
    Go to    ${PLONE_URL}/mydirectory

Log in as site owner and wait
    Log in as site owner
    Wait until page contains    admin

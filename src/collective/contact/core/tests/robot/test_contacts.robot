*** Settings ***
Test Setup        Open SauceLabs test browser
Test Teardown     Run keywords    Report test status    Close all browsers
Resource          plone/app/robotframework/keywords.robot    #Test Setup    Open test browser    #Test Teardown    Close all browsers
Resource          plone/app/robotframework/saucelabs.robot
Resource          keywords.robot

*** Variables ***
${DIVISIONALPHA}    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha
${SERGENT_LH}    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha/regimenth/brigadelh/sergent_lh

*** Test cases ***
Directory is available
    Log in as site owner and wait
    Go to directory
    Page should contain    Military directory

Create a new organization
    Log in as site owner and wait
    Go to directory
    Add new    organization    ${PLONE_URL}/mydirectory
    Input Text    css=#form-widgets-IBasic-title    Squadron five
    Click Button    css=#form-buttons-save
    Page should contain    Squadron five

Can create new contact from organization
    Log in as site owner and wait
    Go to    ${DIVISIONALPHA}
    Page should contain link    css=.addnewcontactfromorganization
    Click link    css=.addnewcontactfromorganization
    Modal is opened
    Wait Until Page Contains Element    css=.modal #oform
    Element should contain    oform-widgets-organization-input-fields    Armée de terre / Corps A / Division Alpha
    Select in livesearch    oform-widgets-person    Ramb
    Element should contain    oform-widgets-person-input-fields    Rambo
    Click button    css=.modal-footer [name="oform.buttons.save"]
    Modal should close

Can create new person from organization
    Log in as site owner and wait
    Go to    ${DIVISIONALPHA}
    Click link    css=.addnewcontactfromorganization
    Modal is opened
    Wait Until Page Contains Element    css=#oform-widgets-person-widgets-query
    Element should not be visible    css=#oform-widgets-person-autocomplete .addnew-block
    Input text    oform-widgets-person-widgets-query    Chuck Norris
    Wait Until Element Is Visible    css=#oform-widgets-person-autocomplete .addnew-block
    Click link    css=#oform-widgets-person-autocomplete .addnew-block a
    Wait Until Page Contains Element    css=#form-widgets-lastname
    Textfield Value Should Be    form-widgets-lastname    Norris
    Textfield Value Should Be    form-widgets-firstname    Chuck
    Click element    form-widgets-gender-0
    Click button    css=.modal-footer [name="form.buttons.save"]
    Wait Until Element Contains    oform-widgets-person-input-fields    Chuck Norris
    Click button    css=.modal-footer [name="oform.buttons.save"]
    Modal should close
    Go to    ${DIVISIONALPHA}
    Wait Until Page Contains Element    other-contacts
    Element Should Contain    other-contacts    Chuck Norris

Can create new organization from the contact form
    Log in as site owner and wait
    Go to    ${PLONE_URL}/mydirectory/@@add-contact
    Wait Until Page Contains Element    css=#oform-widgets-organization-widgets-query
    Input text    oform-widgets-organization-widgets-query    Squadron six
    Wait Until Element Is Visible    css=#oform-widgets-organization-autocomplete .addnew-block
    Click link    css=#oform-widgets-organization-autocomplete .addnew-block a
    Modal is opened
    Wait Until Page Contains Element    css=#form-widgets-IBasic-title
    Textfield Value Should Be    form-widgets-IBasic-title    Squadron six
    Click button    css=.modal-footer [name="form.buttons.save"]
    Modal should close
    Wait Until Element Contains    oform-widgets-organization-input-fields    Squadron six

Can create new contact from position
    Log in as site owner and wait
    Go to    ${SERGENT_LH}
    Page should contain link    css=.addnewcontactfromposition
    Click link    css=.addnewcontactfromposition
    Modal is opened
    Wait Until Page Contains Element    css=#oform-widgets-person-widgets-query
    Element should not be visible    css=#oform-widgets-position-input-fields
    Element should contain    oform-widgets-organization-input-fields    Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH
    Select in livesearch    oform-widgets-person    Ramb
    Wait Until Element Is Visible    css=#oform-widgets-position-input-fields
    Element should contain    oform-widgets-position-input-fields    Sergent de la brigade LH (Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH)

Show parent address if it exists in creation
    Log in as site owner and wait
    Add new    organization    ${PLONE_URL}/mydirectory/armeedeterre/corpsa
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
    Go to edit    ${PLONE_URL}/mydirectory/armeedeterre/corpsa/divisionalpha/capitaine_alpha
    Click link    Address
    Checkbox Should Be Selected    form-widgets-IContactDetails-use_parent_address-0
    Element should contain    css=.address    rue Philibert Lucot
    Element should contain    css=.address    Orléans
    Element should contain    css=.address    France
    Element should not be visible    formfield-form-widgets-IContactDetails-number
    Element should not be visible    formfield-form-widgets-IContactDetails-street
    Element should not be visible    formfield-form-widgets-IContactDetails-city
    Element should not be visible    formfield-form-widgets-IContactDetails-country

Show use parent address checkbox if no parent address when creating a position
    Log in as site owner and wait
    Add new    position    ${PLONE_URL}/mydirectory/armeedeterre/corpsb
    Click link    Address
    Page should contain element    formfield-form-widgets-IContactDetails-number
    Page should contain element    formfield-form-widgets-IContactDetails-street
    Page should contain element    formfield-form-widgets-IContactDetails-city
    Page should contain element    formfield-form-widgets-IContactDetails-country
    Element should be visible    form-widgets-IContactDetails-use_parent_address-0

Don't show use parent address checkbox in edition if no parent address and use parent address is False
    Log in as site owner and wait
    Go to edit    ${PLONE_URL}/mydirectory/armeedeterre/corpsa
    Click link    Address
    Page should contain element    formfield-form-widgets-IContactDetails-number
    Page should contain element    formfield-form-widgets-IContactDetails-street
    Page should contain element    formfield-form-widgets-IContactDetails-city
    Page should contain element    formfield-form-widgets-IContactDetails-country
    Element should not be visible    form-widgets-IContactDetails-use_parent_address-0

Show use parent address checkbox in edition if no parent address and use parent address is True
    Log in as site owner and wait
    Go to edit    ${PLONE_URL}/mydirectory/armeedeterre/corpsb
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

Select in livesearch
    [Documentation]    Type in the search field of a contact widget and select
    ...                the first result.
    [Arguments]    ${widget_id}    ${text}
    Input text    ${widget_id}-widgets-query    ${text}
    Wait Until Element Is Visible    css=#${widget_id}-autocomplete .livesearch-results li.search-result
    Click element    css=#${widget_id}-autocomplete .livesearch-results li.search-result

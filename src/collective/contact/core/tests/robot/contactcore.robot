*** Settings ***
Documentation  collective.contact.core keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.2 syntax (shared with the Plone 4.3 environment).
...            Fixture: test_data profile (setuphandlers.create_test_contact_data).
...            Selectors: this package's templates and collective.contact.widget.
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
${DIRECTORY_URL}  ${PLONE_URL}/mydirectory
${CORPSA}  ${DIRECTORY_URL}/armeedeterre/corpsa
${CORPSB}  ${DIRECTORY_URL}/armeedeterre/corpsb
${DIVISIONALPHA}  ${CORPSA}/divisionalpha
${CAPITAINE_ALPHA}  ${DIVISIONALPHA}/capitaine_alpha
${SERGENT_LH}  ${DIVISIONALPHA}/regimenth/brigadelh/sergent_lh
${DEGAULLE}  ${DIRECTORY_URL}/degaulle
${PEPPER}  ${DIRECTORY_URL}/pepper
@{ADDRESS_FIELDS}  number  street  city  country


*** Keywords ***
Open a manager browser
    Open test browser
    Set window size  1280  2000
    Enable autologin as  Manager

Open the form tab
    [Arguments]  ${label}
    Click link  ${label}

The address fields are in the form
    FOR  ${name}  IN  @{ADDRESS_FIELDS}
        Page should contain element  css=#formfield-form-widgets-IContactDetails-${name}
    END

The parent address is used
    [Documentation]  The checked "use parent address" box shows the address of Corps A, the address fields are hidden
    Checkbox should be selected  css=#form-widgets-IContactDetails-use_parent_address-0
    Element should contain  css=.address  rue Philibert Lucot
    Element should contain  css=.address  Orléans
    Element should contain  css=.address  France
    FOR  ${name}  IN  @{ADDRESS_FIELDS}
        Element should not be visible  css=#formfield-form-widgets-IContactDetails-${name}
    END

The use parent address checkbox is visible
    [Arguments]  ${expected}=${True}
    Run keyword if  ${expected}  Element should be visible  css=#form-widgets-IContactDetails-use_parent_address-0
    ...  ELSE  Element should not be visible  css=#form-widgets-IContactDetails-use_parent_address-0

Click the create contact link
    [Documentation]  "Create Contact" link of an organization or position view: opens the contact form in a modal
    Click link  css=.addnewcontactfromorganization, .addnewcontactfromposition
    The modal is open
    Wait until page contains element  css=#oform-widgets-person-widgets-query

Type in the contact widget
    [Arguments]  ${widget_id}  ${text}
    Input text  css=#${widget_id}-widgets-query  ${text}

The contact widget value contains
    [Arguments]  ${widget_id}  ${text}
    Wait until element contains  css=#${widget_id}-input-fields  ${text}

Click the add new link of the contact widget
    [Documentation]  "Create ..." link shown under a contact widget: opens the add form in a modal
    [Arguments]  ${widget_id}
    Wait until element is visible  css=#${widget_id}-autocomplete .addnew-block
    Click link  css=#${widget_id}-autocomplete .addnew-block a

The textfield value becomes
    [Documentation]  For values filled by javascript
    [Arguments]  ${locator}  ${value}
    Wait until keyword succeeds  10s  0.5s  Textfield value should be  ${locator}  ${value}

The prefilter of the contact widget is
    [Arguments]  ${widget_id}  ${label}
    List selection should be  css=#${widget_id}-autocomplete .prefilter-select  ${label}

Select the prefilter of the contact widget
    [Arguments]  ${widget_id}  ${label}
    Select from list by label  css=#${widget_id}-autocomplete .prefilter-select  ${label}

Open the test type add form
    Go to  ${PLONE_URL}
    Add new  testtype

The other contacts contain
    [Arguments]  ${organization_url}  ${text}
    Go to  ${organization_url}
    Wait until element contains  css=#other-contacts  ${text}

Held position
    [Documentation]  Locator of the block of a held position (by title) in the person view
    [Arguments]  ${title}
    [Return]  xpath=//div[@id="held_positions"]/div[contains(@class, "held_position")][.//h3/span[contains(normalize-space(.), "${title}")]]

Click the held position link
    [Documentation]  view, edit or delete link of a held position (by title) in the person view
    [Arguments]  ${title}  ${link}
    ${held_position}=  Held position  ${title}
    Click link  ${held_position}//a[contains(@class, "${link}-held-position")]

The held position icon is the held position type icon
    [Arguments]  ${title}
    ${held_position}=  Held position  ${title}
    ${icon}=  Type icon file  held_position
    Page should contain element  ${held_position}//h3/img[substring(@src, string-length(@src) - string-length("${icon}") + 1) = "${icon}"]

Click the edit link of the content
    [Documentation]  Edit link of the basefields (organization, person, position, held position views): opens a modal
    Click link  css=.actions a[class^="edit-"]
    The modal is open

The vcard of the contact is downloadable
    [Documentation]  "Download VCard" link of the contact details, and its vcf content
    [Arguments]  ${url}  ${name}
    Page should contain element  css=#download_vcard a[href$="${url}/@@contact.vcf"]
    ${vcard}=  Execute javascript
    ...  var xhr = new XMLHttpRequest(); xhr.open('GET', '${url}/@@contact.vcf', false); xhr.send(); return xhr.responseText;
    Should contain  ${vcard}  BEGIN:VCARD
    Should contain  ${vcard}  ${name}

The sub-organizations contain
    [Arguments]  ${text}
    Element should contain  css=#sub_organizations  ${text}

Hover the sub-organization link
    [Arguments]  ${title}
    Mouse over  xpath=//*[@id="sub_organizations"]//a[contains(@class, "link-tooltip")][normalize-space(.)="${title}"]

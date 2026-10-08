*** Keywords ***
a Site Owner
    Log in as site owner

a French Plone site
    Go to  ${PLONE_URL}/@@language-controlpanel
    Select From List  form.default_language  fr
    Click Button  form.actions.save

Add new
    [Documentation]    Open the add form of a content type in a container (the
    ...                add menu of the toolbar has no stable locator).
    [Arguments]   ${name}    ${container}=${PLONE_URL}
    Go to  ${container}/++add++${name}
    Wait Until Page Contains Element  css=#form

Go to edit
    [Arguments]   ${url}
    Go to  ${url}/edit
    Wait Until Page Contains Element  css=#form

Modal is opened
    Wait Until Page Contains Element  css=.modal

Modal should close
    Wait Until Page Does Not Contain Element  css=.modal

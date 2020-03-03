*** Keywords ***
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
    Wait Until Page Contains Element  css=#form

Close Overlay
    Click Element  css=div.overlay div.close

Overlay should close
    Element should not remain visible  id=exposeMask
    Wait until keyword succeeds  60  1  Page should not contain element  css=div.overlay

Person overlay should close
    Wait until page contains element  oform

Overlay is opened
    Wait Until Page Contains Element  css=.overlay

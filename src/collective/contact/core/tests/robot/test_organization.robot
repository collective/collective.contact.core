*** Settings ***
Documentation  Organization view (basefields, sub-organizations).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactcore.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
The edit link of an organization opens its edit form
    Go to  ${CORPSB}
    Click the edit link of the content
    ${title}=  Modal element  form-widgets-IBasic-title
    Input text  ${title}  Corps C
    Click the modal button  form.buttons.save
    The modal is closed
    Wait until element contains  css=#content h1  Armée de terre / Corps C

The organization description is shown on its view
    Go to  ${CORPSB}
    Click the edit tab
    Input text  css=#form-widgets-IBasic-description  Second army corps
    Click button  css=#form-buttons-save
    The status message contains  Changes saved
    Element should contain  css=#content  Second army corps

A sub-organization can be created from an organization
    Go to  ${CORPSB}
    Add new  organization
    Input text  css=#form-widgets-IBasic-title  Division Gamma
    Click button  css=#form-buttons-save
    Wait until element contains  css=#content h1  Armée de terre / Corps B / Division Gamma
    Go to  ${CORPSB}
    The sub-organizations contain  Division Gamma

Hovering a sub-organization link shows that organization in a tooltip
    Go to  ${CORPSA}
    Hover the sub-organization link  Division Alpha
    The tooltip shows the organization  Armée de terre / Corps A / Division Alpha

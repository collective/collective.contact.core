*** Settings ***
Documentation  Directory, organizations and contacts (held positions) creation, parent address.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactcore.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
Directory is available
    Go to  ${PLONE_URL}
    Click the portal tab  mydirectory
    Wait until page contains  Military directory
    Location should be  ${DIRECTORY_URL}

Create a new organization
    Go to  ${DIRECTORY_URL}
    Add new  organization
    Input text  css=#form-widgets-IBasic-title  Squadron five
    Click button  css=#form-buttons-save
    Wait until page contains  Squadron five
    Go to  ${DIRECTORY_URL}
    Element should contain  css=#organizations  Squadron five

Can create new contact from organization
    Go to  ${DIVISIONALPHA}
    Click the create contact link
    The contact widget value contains  oform-widgets-organization  Armée de terre / Corps A / Division Alpha
    Select in the contact widget  oform-widgets-person  Ramb
    The contact widget value contains  oform-widgets-person  Rambo
    Click the modal button  oform.buttons.save
    The modal is closed
    The other contacts contain  ${DIVISIONALPHA}  Rambo

Can create new person from organization
    Go to  ${DIVISIONALPHA}
    Click the create contact link
    Element should not be visible  css=#oform-widgets-person-autocomplete .addnew-block
    Type in the contact widget  oform-widgets-person  Chuck Norris
    Click the add new link of the contact widget  oform-widgets-person
    Wait until element is visible  css=#form-widgets-lastname
    The textfield value becomes  css=#form-widgets-lastname  Norris
    The textfield value becomes  css=#form-widgets-firstname  Chuck
    Click element  css=#form-widgets-gender-0
    Click the modal button  form.buttons.save
    The contact widget value contains  oform-widgets-person  Chuck Norris
    Click the modal button  oform.buttons.save
    The modal is closed
    The other contacts contain  ${DIVISIONALPHA}  Chuck Norris

Can create new organization from the contact form
    Go to  ${DIRECTORY_URL}/@@add-contact
    Wait until page contains element  css=#oform-widgets-organization-widgets-query
    Type in the contact widget  oform-widgets-organization  Squadron six
    Click the add new link of the contact widget  oform-widgets-organization
    The modal is open
    The textfield value becomes  css=#form-widgets-IBasic-title  Squadron six
    Click the modal button  form.buttons.save
    The modal is closed
    The contact widget value contains  oform-widgets-organization  Squadron six

Can create new contact from position
    Go to  ${SERGENT_LH}
    Click the create contact link
    Element should not be visible  css=#oform-widgets-position-input-fields
    The contact widget value contains  oform-widgets-organization  Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH
    Select in the contact widget  oform-widgets-person  Ramb
    Wait until element is visible  css=#oform-widgets-position-input-fields
    Element should contain  css=#oform-widgets-position-input-fields  Sergent de la brigade LH (Armée de terre / Corps A / Division Alpha / Régiment H / Brigade LH)
    Click the modal button  oform.buttons.save
    The modal is closed

Can create new contact with the add held position form
    Go to  ${DIRECTORY_URL}/@@add-held-position
    Select in the contact widget  oform-widgets-organization  Corps B
    Select in the contact widget  oform-widgets-person  Pepper
    Click button  css=#oform-buttons-save
    The status message contains  Item created
    Go to  ${PEPPER}
    Element should contain  css=#held_positions  Corps B

The add organization form opens the selected organization
    Go to  ${DIRECTORY_URL}/@@add-organization
    Select in the contact widget  oform-widgets-organization  Corps B
    Click button  css=#oform-buttons-save
    Location should be  ${CORPSB}

Show parent address if it exists in creation
    Go to  ${CORPSA}
    Add new  organization
    Open the form tab  Address
    The parent address is used

Show parent address if it exists in edition
    Go to  ${CAPITAINE_ALPHA}
    Click the edit tab
    Open the form tab  Address
    The parent address is used

Show use parent address checkbox if no parent address when creating a position
    Go to  ${CORPSB}
    Add new  position
    Open the form tab  Address
    The address fields are in the form
    The use parent address checkbox is visible

Don't show use parent address checkbox in edition if no parent address and use parent address is False
    Go to  ${CORPSA}
    Click the edit tab
    Open the form tab  Address
    The address fields are in the form
    The use parent address checkbox is visible  ${False}

Show use parent address checkbox in edition if no parent address and use parent address is True
    Go to  ${CORPSB}
    Click the edit tab
    Open the form tab  Address
    The address fields are in the form
    The use parent address checkbox is visible

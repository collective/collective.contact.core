*** Settings ***
Documentation  Person view (basefields, contact details, held positions) and person form.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactcore.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Variables ***
${SERGENT_PEPPER}  Sergent de la brigade LH


*** Test Cases ***
The held positions of a person link to their view
    Go to  ${PEPPER}
    Click the held position link  ${SERGENT_PEPPER}  zoom
    Location should be  ${PEPPER}/sergent_pepper/view
    Element should contain  css=#content  ${SERGENT_PEPPER}

The held positions of a person link to their edit form
    Go to  ${PEPPER}
    Click the held position link  ${SERGENT_PEPPER}  edit
    Wait until page contains element  css=#form
    Location should be  ${PEPPER}/sergent_pepper/edit

A held position can be deleted from the person view
    Go to  ${PEPPER}
    Click the held position link  ${SERGENT_PEPPER}  delete
    Confirm the deletion
    The status message contains  has been deleted
    Go to  ${PEPPER}
    Page should not contain element  css=#held_positions

The held positions of a person show the held position icon
    Go to  ${PEPPER}
    The held position icon is the held position type icon  ${SERGENT_PEPPER}

The edit link of a person opens its edit form
    Go to  ${PEPPER}
    Click the edit link of the content
    ${lastname}=  Modal element  form-widgets-lastname
    Input text  ${lastname}  Salt
    Click the modal button  form.buttons.save
    The modal is closed
    Wait until element contains  css=#content h1  Mister Salt

The person title is prefilled from the gender
    Go to  ${DIRECTORY_URL}
    Add new  person
    Click element  css=#form-widgets-gender-1
    The textfield value becomes  css=#form-widgets-person_title  Mrs
    Click element  css=#form-widgets-gender-0
    The textfield value becomes  css=#form-widgets-person_title  Mr
    Input text  css=#form-widgets-person_title  Doctor
    Click element  css=#form-widgets-gender-1
    Sleep  1
    Textfield value should be  css=#form-widgets-person_title  Doctor

A contact offers its vcard for download
    Go to  ${PEPPER}
    The vcard of the contact is downloadable  ${PEPPER}  FN:Mister Pepper

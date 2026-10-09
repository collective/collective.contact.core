*** Settings ***
Documentation  Prefilter of the contact widget (testing.IPrefiltering behavior of the testtype).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactcore.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Variables ***
${NO_DEFAULT}  form-widgets-IPrefiltering-contact_list_no_default
${WITH_DEFAULT}  form-widgets-IPrefiltering-contact_list_with_contextual_default


*** Test Cases ***
With and without default value
    Open the test type add form
    The prefilter of the contact widget is  ${NO_DEFAULT}  No filter
    The prefilter of the contact widget is  ${WITH_DEFAULT}  Only organizations

Without prefilter
    Open the test type add form
    Type in the contact widget  ${NO_DEFAULT}  Pepper
    The contact widget results contain  ${NO_DEFAULT}  Pepper

With prefilter
    Open the test type add form
    Type in the contact widget  ${WITH_DEFAULT}  Pepper
    Sleep  5
    The contact widget results do not contain  ${WITH_DEFAULT}  Pepper

Selecting another prefilter
    Open the test type add form
    Select the prefilter of the contact widget  ${WITH_DEFAULT}  Only people
    Type in the contact widget  ${NO_DEFAULT}  Pepper
    The contact widget results contain  ${NO_DEFAULT}  Pepper

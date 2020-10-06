*** Settings ***
Test Setup        Open SauceLabs test browser
Test Teardown     Run keywords    Report test status    Close all browsers
Resource          plone/app/robotframework/keywords.robot    #Test Setup    Open test browser    #Test Teardown    Close all browsers
Resource          plone/app/robotframework/saucelabs.robot
Resource          keywords.robot


*** Test cases ***
With and without default value
    Add test type
    List Selection Should Be  css:#form-widgets-IPrefiltering-contact_list_no_default-autocomplete .prefilter-select  No filter
    List Selection Should Be  css:#form-widgets-IPrefiltering-contact_list_with_contextual_default-autocomplete .prefilter-select  Only organizations

Without prefilter
    Add test type
    Input Text  css:#form-widgets-IPrefiltering-contact_list_no_default-widgets-query  Pepper
    Autocomplete results should contain  Pepper

With prefilter
    Add test type
    Input Text  css:#form-widgets-IPrefiltering-contact_list_with_contextual_default-widgets-query  Pepper
    Sleep  5
    Autocomplete results should not contain  Pepper

Selecting another prefilter
    Add test type
    Select From List By Label  css:#form-widgets-IPrefiltering-contact_list_with_contextual_default-autocomplete .prefilter-select  Only people
    Input Text  css:#form-widgets-IPrefiltering-contact_list_no_default-widgets-query  Pepper
    Autocomplete results should contain  Pepper


*** Keywords ***
Go to directory
    Go to    ${PLONE_URL}/mydirectory

Log in as site owner and wait
    Log in as site owner
    Wait until page contains    admin

Add test type
    Log in as site owner and wait
    Go to    ${PLONE_URL}
    Add new    testtype

Autocomplete results should contain
    [Arguments]    ${value}
    Wait Until Element Is Visible  xpath://div[@class="ac_results"]
    Element Should Be Visible  xpath://div[@class="ac_results"]/ul/li/strong[text()='${value}']

Autocomplete results should not contain
    [Arguments]    ${value}
    Page Should Not Contain Element  xpath://div[@class="ac_results"]/ul/li/strong[text()='${value}']

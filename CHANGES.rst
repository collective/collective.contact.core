Changelog
=========

1.1 (unreleased)
----------------

- Don't crash when deleting position or organization if a held position is
  associated with it. Show relations that will be broken
  (plone.app.linkintegrity integration).
  [vincentfretin]

- Fix ObjectModifiedEvent subscribers to not reindex if event is
  a ContainerModifiedEvent.
  [vincentfretin]

- Don't show use_parent_address checkbox if there is no parent address.
  [cedricmessiant]

- Fix parent address in add forms.
  [cedricmessiant]

- Add more robot framework tests.
  [cedricmessiant]

- Add 'Create Contact' link on position view.
  [cedricmessiant]

- Use full title instead of Title in position view title.
  [cedricmessiant]

- Show organization's and root organization's name in position's full title.
  [cedricmessiant]

- Add first organization title in held position's title.
  [cedricmessiant]

- Added logo and activity rich field on organization type.
  [thomasdesvenain]

- Fixed generate id from title on held positions and persons.
  [thomasdesvenain]

- When we get the address of a contact, if the most direct address is empty,
  look for the next.
  [thomasdesvenain]

- Added Fax and Website fields to IContactDetails and IContactable.
  [thomasdesvenain]

- Fixed javascript in @@add-organization view.
  [vincentfretin]

- Fixed use parent address if we set Contact Details behaviour on held positions.
  [thomasdesvenain]

- Add vCard support to organizations
  [ebrehault]

1.0 (2013-09-13)
----------------

- Birthday is now optional as a behaviour.
  [thomasdesvenain]

- Use (-200, 1) years range for birthday field.
  [vincentfretin]

- "Add new" popup link is renamed from "Add ..." to "Create ..."
  [thomasdesvenain]

- New behaviour to add a "Related organizations" field on a content type.
  [thomasdesvenain]

- Plain text search improvements :
    - we can find persons with organization names, functions names,
    - the same for held positions,
    - indexation is updated when organization or function changes
  [thomasdesvenain]

- Messages that document better the organization / position held position
  adding process.
  [thomasdesvenain]

- Display position label in title of held position view page.
  [thomasdesvenain]

- Added an additional input text label to held positions,
  used on titles if held_position is directly related to an organization.
  [thomasdesvenain]

- Display contacts on organization page.
  [thomasdesvenain]

- We can find a function with the organization name.
  [thomasdesvenain]

- Fixed field customization view.
  [vincentfretin, thomasdesvenain]

- Fixed held_position field showing in Add contact overlay if Plone site id
  is different of Plone.
  [vincentfretin]

- Added workflows for contact objects.
  [cedricmessiant]


0.11 (2013-03-11)
-----------------

- Fixed bug with default views.
  [cedricmessiant]


0.10 (2013-03-07)
-----------------

- Fixed MANIFEST.in
  [cedricmessiant]


0.9 (2013-03-07)
----------------

- Initial release
  [cedricmessiant]


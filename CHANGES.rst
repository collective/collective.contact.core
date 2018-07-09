Changelog
=========

1.19 (2018-07-09)
-----------------

- Add email to SearchableText of a person. Useful when fixing contact data for
  smtp error reports after sending a newsletter with collective.contact.mailaction
  [fRiSi]

1.18 (2018-06-07)
-----------------

- Use real full title in held_position and position get_full_title methods.
  Necessary to display to the end user the right organization, without ambiguity.
  [sgeulette]

- Prevent address fields from being erased if they are changed programmaticaly before any manual edition.
  [thomasdesvenain]

- Prevent title ascii error on organization vcard export.
  [bsuttor]

- Prevent fatal error if there is no organization on held_position.
  [thomasdesvenain]

- Prevent error when person is None on held_position.
  [Gagaro]

- Use another version than 1.2.8 for plone.app.textfield as version 1.2.9
  fixes issue we had in tests.
  (See https://github.com/plone/plone.app.textfield/issues/22).
  [gbastien]

- Display positions on the organization view respecting order (getObjPositionInParent).
  [gbastien]

- Display various content title consistently everywhere in the application.
  [gbastien, sgeulette]

- Display content icon before content title.
  [gbastien]

- Added parameter display_contact_photo_on_organization_view to the registry,
  it True (default), the contact photo is displayed in the @@othercontacts, if
  False, the person content_type icon is displayed.
  [gbastien]

1.17 (2017-10-02)
-----------------

- Fix get_valid_url mehtod when there is accent into url.
  [bsuttor]


1.16 (2017-09-22)
-----------------

- Set person_contact_details_private option to true by default.
  [sgeulette]

1.15 (2017-05-30)
-----------------

- Fix robot tests.
  [thomasdesvenain]

- Don't purge behaviors when reinstalling.
  [sgeulette]

- Set plone.app.textfield maximum version as 1.2.7
  [thomasdesvenain]


1.14 (2017-05-16)
-----------------

- Lint for code-analysis.
  [bsuttor]


1.13 (2017-05-16)
-----------------

- Set IContactDetails behavior on held_position type.
  Person contact details are considered as personal data.
  [sgeulette]

- Use a python view to provide gender/person title mapping. In this way, the terms can be translated.
  [cedricmessiant]

- Avoid error in addcontact when there is no directory.
  [cedricmessiant]

- Prevent fatal error if by chance a held position related to a position or an organisation has been removed
  but the relation always exist. An error is logged.
  [thomasdesvenain]

- Refactor: move complex sortable title methods into content objects.
  [thomasdesvenain]


1.12 (2017-01-17)
-----------------

- Change field order for address (`<street> <nr>` - as this is more common in most countries)

  * address format can be localized by using msgid `address_line`
  * field order in add and edit forms can be patched (see README for details)

  (fixes #29) [fRiSi]

- Fixed indexing a held position which organization has been removed.
  [thomasdesvenain]

- Add translations for de, it, fr and sl.
  [fRiSi]

1.11 (2016-10-13)
-----------------

- Fix setup_relation_dependency when many are setup on the same page.
  [thomasdesvenain]

- Fix "create contact" widget link when master organization field value has
  changed or has become empty.
  [thomasdesvenain]

1.10 (2016-10-05)
-----------------

- Fix AddContact form problem with security hotfix 20160830
  [ebrehault]

1.9 (2016-07-07)
----------------

- Reindex suborganizations (and positions and held positions) when an
  organization is modified.
  [vincentfretin]

- Use start and end indexes for held_position.
  [sgeulette]

1.8 (2016-03-31)
----------------

- Hide contact types from the navigation.
  [pcdummy]

- Sort sub organizations by folder position in organization view
  [sgeulette]

1.7 (2016-03-04)
----------------

- Do not hide token column in edit mode
  [sgeulette]

- Expose person_title in held_position
  [ebrehault]

1.6 (2015-11-24)
----------------

- Fix slave field creation button for held positions
  [ebrehault]

- Fix organization searchable text when related organizations
  [ebrehault]

- Allow reorder on directory fields
  [cedricmessiant]

- Fix prelabel_for_portal_type signature.
  Some javascript fixes or improvements.
  [vincentfretin]

- Use different views/schemas for different use cases for add-contact widget
  [cedricmessiant]

1.5 (2015-06-02)
----------------

- Feature: Display held positions start date and end date on organization view.
  [cedricmessiant]

- Feature: Add custom settings to override prelabel and label of the 'Create' link in widget.
  [cedricmessiant]

- Added italian translation
  [keul]

- JSLint fixes (invalid commas)
  [keul]

1.4 (2015-04-03)
----------------

- Fix javascript that was disabled by error in addcontact view.

- Feature: Add parameter to choose if we want to use description to search
  persons.
  [cedricmessiant]

- UI: Turn phone numbers into clickable tel: links.
  [jazwsophie]

- Feature: Add parameter to choose if we want to use held positions to search
  persons.
  [cedricmessiant]


1.3 (2014-09-11)
----------------

- Feature: Simple validator for phone number.
  [thomasdesvenain]

- UI: If website doesn't start with http, add http:// at its beginning.
  [cedricmessiant]

- UI: Open external web site in a new window.
  [vincentfretin]

- UI: Avoid the contact information of a person be displayed two times
  when it fall backs from organization or function.
  [thomasdesvenain]

- UI: If a contact field is dependent to a position or an organization,
  we update 'add new' link of the contact field
  so that the 'position' or 'organization' field is pre-selected in the overlay.
  [thomasdesvenain]

- UI: use classes instead of ids on address because it can be used
  several times on the same page.
  [thomasdesvenain]

- API: added a nonfallbackcontactdetails view that displays only direct contact details.
  Useful when you want to display contact details of a contact and contact details
  of objects it is related to on the same page: it avoids double displays.
  Apply it on held positions view.
  [thomasdesvenain]

- Fix: If held position implements IContactDetails behavior,
  then show contact details fields on add contact form.
  [thomasdesvenain]

- Fix: If 'use parent address' has been selected,
  ensure content address fields are cleared.
  [thomasdesvenain]

- Fix: Hide use parent address:
     - works in overlays,
     - always display use parent address on held position if it implements contact details.

  [thomasdesvenain]

- Fix: Avoid failure on person
  if for any reason person title, firstname or lastname attribute is not set.
  [thomasdesvenain]

- Fix: Switch street and additional data on address view.
  [thomasdesvenain]

- Fix: address fallback in excel export.
  [thomasdesvenain]

- Fix: VCard - avoid failure if no 'person_title' is set on content.
  [thomasdesvenain]

- Fix: Contact might not have any aq_parent
  [ebrehault]

- Hide 'Use parent address' checkbox only if it is not checked and if parent
  address is empty
  [ebrehault]


1.2 (2014-06-16)
----------------

- Contact details of a person fallbacks to person's main position
  get from IPersonHeldPositions adapter.
  [thomasdesvenain]

- Added an IPersonHeldPositions adapter that gets positions sorted by status :
  a main position, all current positions, closed positions.
  [thomasdesvenain]

- Sort get_held_positions on organization.
  [cedricmessiant]

- Add plone.abovecontenttitle viewlet manager to person, organization, position
  and contact (held_position) views.
  [vincentfretin]

- js functions have a namespace.
  [thomasdesvenain]

- Add an api to make dependencies between a contact field and an other one.
  (needs collective.contact.widget >= 1.2)
  [thomasdesvenain]

- Add parameter to choose if we want to display person title in person's displayed title.
  [cedricmessiant]

- Tools for excel export with collective.excelexport:
  - renderer for contact field,
  - exportable to show person infos on held_position export.
  [thomasdesvenain]


1.1 (2014-03-11)
----------------

- Remove meta_type override because it breaks copy support.
  [thomasdesvenain]

- Fix if for any reason use_parent_address is True, content has an address and
  has no parent with an address.
  [thomasdesvenain]

- Add help messages on add contact form.
  [thomasdesvenain]

- Display more information about "other contacts" in organization view.
  [cedricmessiant]

- Add ICustomSettings adapter lookup in widget settings utility to be
  able to overrides add_url_for_portal_type method in some projects.
  [vincentfretin]

- Rewrite every contact content view in separate views (basefields, contactdetails, etc) so
  that we can override only a specific part of the view in customer projects.
  [cedricmessiant]

- Rename all contact content views to "view".
  [cedricmessiant]

- Add hcard microformat (see http://microformats.org/wiki/hcard) for person and organization.
  [cedricmessiant]

- Use a macro to display contact details.
  [thomasdesvenain]

- Manage case users have uploaded non-image formats for logo or photo.
  [thomasdesvenain]

- Display behavior fields on contactable views
  once they are in default fieldset.
  [thomasdesvenain]

- Fixed: keep order of TTW fields displayed on view pages.
  [thomasdesvenain]

- Add tooltip overviews for held positions, persons, positions and organizations.
  [cedricmessiant]

- Use thumb scale for logos and photos.
  [cedricmessiant]

- Add icon for 'Create Contact' link on position and organization pages.
  [cedricmessiant]

- Customize sortable_title indexer for Person and Held Position
  and add a corresponding brain
  metadata (to enable use of this index in collective.contact.facetednav
  alphabetic search widget).
  [cedricmessiant]

- A content that just implements IContactDetails behavior
  is adaptatable to IContactable and have a VCal export.
  [thomasdesvenain]

- We can hide Use parent address field using a permission:
  "collective.contact.core.UseParentAddress"
  So it is possible to remove this feature via rolemap
  or remove it on some content types via workflow.
  [thomasdesvenain]

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

- Plain text search improvements:
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

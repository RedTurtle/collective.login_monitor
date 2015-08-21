Changelog
=========

0.4 (2015-08-21)
----------------

- Added a contact form, for sending ad email message to all users found by the search
  [keul]
- Added an (hidden) export to JSON feature. 3rd party add-ons can use this for performing
  operation of search results
  [keul]
- Search view is now "callable" with custom parameters
  [keul]
- Added a negative search filter, for looking for users who didn't logged in
  in the given range.
  *Please note* that users must still be indexed by the table (a user who never logged in
  will not be found)
  [keul]
- Added search filter by user id
  [keul]
- Added new information about last login date of the user
  [keul]
- Fixed errors in foreign key definition on schema models
  [keul]

0.3.1 (2014-11-06)
------------------

- Fixed date error in that will be raised in some cases
  [keul]
- React to a wider range of problems when database connection
  is not working
  [keul]

0.3 (2014-10-28)
----------------

Dropped Plone 3 compatibility

- Add Full Name and E-mail columns to the search results and CSV output.
  [davidjb]
- Fix selected Group logic on search form.
  [davidjb]
- Clarify description for group selection field.
  [davidjb]
- Minor grammar update for column headings on search page and export.
  [davidjb]
- Change icon URLs to use PNG format rather than deprecated GIF images.
  [davidjb]
- Add exception handling in the event, if no db is configured [cekk]

0.2 (2013-04-18)
----------------

First public release

* old code totally refactored (removed ``sqldict`` for a pure ``SQLAlchemy`` approach)
  [keul]
* i18n support
  [keul]

0.1 (unreleased)
----------------

- Initial release

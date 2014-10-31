Changelog
=========

0.3.1 (unreleased)
------------------

- Fixed date error in that will be raised in some cases
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
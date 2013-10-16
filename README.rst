Save any **login operation** done in your Plone site to an external database and provide a Plone interface
for query the database.

.. contents:: **Table of contents**

Introduction
============

This Plone add-on is based on `z3c.saconfig`__ and `SQLAlchemy`__, and can't provide any new feature to Plone
without a propert configuration.

__ http://pypi.python.org/pypi/z3c.saconfig
__ http://sqlalchemy.org/

Keep reading for installation and configuration guide.

How to use
==========

After the installation, any login done in your Plone will save to an external database an entry that store:

* user id
* a timestamp

Then a new configuration panel can bhe found in the site configuration: "*Monitor user logins*".

From this view you can query the database previously populated:

.. image:: http://blog.redturtle.it/pypi-images/collective.login_monitor/collective.login_monitor-0.2-01.png 
   :alt: Control panel for login monitor

You must limit the search inside a rande of dates, and optionally limiting users to members of a group.
Results of the table displayed can be export to a CSV file.

Multiple sites
--------------

If your buildout hosts multiple Plone sites, all of them will store data in the database keeping same username
on different sites separated.

Installation and configuration
==============================

You must configure an access to an external DBMS. The name of the engine used must be ``plone_logins``.

Follow an example based on `sqlite`__ (**not advised for production environment**).

__ http://www.sqlite.org/

Add ``collective.login_monitor`` to your buildout, then provide a SQLAlchemy connection string:

.. code-block:: ini

    [buildout]
    ...
    
    [instance]
    ...
    eggs=
       ...
       collective.login_monitor
    
    zcml-additional =
        ...
        <configure xmlns="http://namespaces.zope.org/zope"
                  xmlns:db="http://namespaces.zope.org/db">
           <include package="z3c.saconfig" file="meta.zcml" />
           <db:engine name="plone_logins"
                      url="sqlite:///${buildout:directory}/var/filestorage/plone_logins.db"
                      setup="collective.login_monitor.prepare_model.prepare"
                      />
           <db:session name="plone_logins" engine="plone_logins" />
       </configure>

Credits
=======

Developed with the support of:

* `Azienda USL Ferrara`__
  
  .. image:: http://www.ausl.fe.it/logo_ausl.gif
     :alt: Azienda USL's logo
  
* `S. Anna Hospital, Ferrara`__

  .. image:: http://www.ospfe.it/ospfe-logo.jpg 
     :alt: S. Anna Hospital - logo

All of them supports the `PloneGov initiative`__.

__ http://www.ausl.fe.it/
__ http://www.ospfe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

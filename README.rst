.. contents::

Introduction
============

This add-on is part of the ``collective.contact.*`` suite. For an overview and a demo of these suite, see `collective.contact.demo <https://github.com/collective/collective.contact.demo>`__.

A Plone add-on that provides a directory where you create persons, organizations, sub-organizations and positions.


How-to
======

First, create a directory in your site. This directory will contain all the informations related to your contacts.

You can then add organizations to his directory. An organization can contain organizations (such as services, divisions or department) or positions (such as CEO, mayor or developer).

You can also add persons to this directory. A person is a physical person that can hold one or more positions or be member of one or more organizations. To associate a person with an organization or a position, add a held position content type in the person's context.

Modify your directory to customize the organization types and the position types that you will associate with your organizations, sub-organizations and positions.

Look at the test data profile collective.contact.core test data for detailed examples.

Installation
============

* Add collective.contact.core to your eggs.
* Re-run buildout.
* Install the product in your plone site.

Tests
=====

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://secure.travis-ci.org/collective/collective.contact.core.png
    :target: http://travis-ci.org/collective/collective.contact.core

Credits
=======

Have an idea? Found a bug? Let us know by `opening a ticket`_.

.. _`opening a ticket`: https://github.com/collective/collective.contact.core/issues

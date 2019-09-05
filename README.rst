.. contents::

Introduction
============

This add-on is part of the ``collective.contact.*`` suite. For an overview and a demo of these suite, see `collective.contact.demo <https://github.com/collective/collective.contact.demo>`__.

A Plone add-on that provides a directory where you create persons, organizations, sub-organizations and positions.


How-to
======

First, create a directory in your site. This directory will contain all the informations related to your contacts.

You can then add organizations to this directory. An organization can contain organizations (such as services, divisions or department) or positions (such as CEO, mayor or developer).

You can also add persons to this directory. A person is a physical person that can hold one or more positions or be member of one or more organizations.
To associate a person with an organization or a position, add a held position content type in the person's context.

Consider the following:

* the person type will contain personal contact details
* the held_position type will contain professional contact details

Modify your directory to customize the organization types and the position types that you will associate with your organizations, sub-organizations and positions.

Look at the test data profile collective.contact.core test data for detailed examples.


Configuration
=============

The following configuration can be adapted in the plone registry (prefix=IContactCoreParameters):

* person_contact_details_private : boolean, default to True.
    The person contact details are private and will not be used in other context, like held position.
* person_title_in_title : boolean, default to True.
    Display person title in displayed person's title.
* use_held_positions_to_search_person : boolean, default to True.
    Use held positions to search persons.
* use_description_to_search_person : boolean, default to True.
    Use description to search persons.
* display_contact_photo_on_organization_view : boolean, default to True.
    Display contact photo on organization view.
* contact_source_metadata_content : choice, default to get_full_title.
    Choose information displayed after a search in contact widget.

Localization
============

In some countries (i.e. France) the format of an address is `<nr> <street>` instead of `<street> <nr>`.

You can provide a translation for the `address_line` i18n-msgid in the collective.contact.core translations if this is the case for your country.

You can also patch `collective.contact.core.behaviors.ADDRESS_FIELDS` to make the number field show up before the street in add and edit forms.

In your addon, create a `patches.py` file with this content::

    from collective.contact.core import behaviors
    behaviors.ADDRESS_FIELDS[0:2] = reversed(behaviors.ADDRESS_FIELDS[0:2])
    behaviors.ADDRESS_FIELDS_PLUS_PARENT[2:4] = reversed(behaviors.ADDRESS_FIELDS_PLUS_PARENT[2:4])

and import it in yout `__init__.py` so the patches takes effect.


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

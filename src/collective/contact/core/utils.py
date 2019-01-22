# encoding: utf-8

from collective.contact.core.content.person import IPerson
from collective.contact.core.interfaces import IHeldPosition


def get_gender_and_number(contacts):
    """Return gender and number of given contacts.
       Returns None if not genderable.
       Returns a 2 letters code if genderable:
       - first letter is for gender, M for "male", "F" for female;
       - second letter is for number, S for "Singular", "P" for "Plural".
       p_contacts may be any kind of contacts, we will try to get person of it."""
    gender = None
    number = 0
    # make sure we do not have several times same person even thru held_position
    person_uids = []
    for contact in contacts:
        person = None
        if IHeldPosition.providedBy(contact):
            person = contact.get_person()
        elif IPerson.providedBy(contact):
            person = contact
        if person:
            person_uid = person.UID()
            if person_uid in person_uids:
                continue
            else:
                person_uids.append(person_uid)
            person_gender = person.gender
            if person_gender in [u'M', u'F']:
                number = number + 1
            # "M" takes priority, if already found, we keep it
            if gender != 'M':
                gender = person_gender
    res = gender
    if gender:
        res = gender + (number > 1 and 'P' or 'S')
    return res

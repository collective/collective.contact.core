from five import grok

from zope.lifecycleevent.interfaces import IObjectAddedEvent

from collective.contact.widget.interfaces import IContactContent


@grok.subscribe(IContactContent, IObjectAddedEvent)
def set_is_created(obj, event):
    obj.is_created = True

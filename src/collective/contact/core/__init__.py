from zope.i18nmessageid import MessageFactory

import logging
logger = logging.getLogger('collective.contact.core')

_ = MessageFactory("collective.contact.core")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

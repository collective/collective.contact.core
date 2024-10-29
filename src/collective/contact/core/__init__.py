from imio.fpaudit import utils
from plone import api
from zope.i18nmessageid import MessageFactory

import logging
import os


logger = logging.getLogger('collective.contact.core')

_ = MessageFactory("collective.contact.core")

if os.environ.get("ZOPE_HOME") is None:  # test env
    # for a function to patch, it is needed to do it before importing the module
    # mock.patch is not working in this case
    logged_actions = []

    def mock_fplog(log_id, action, extras):
        logged_actions.append(extras)

    logger.warn("PATCHING imio.fpaudit.utils.fplog")
    utils.fplog = mock_fplog


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


def _tr(msgid):
    return api.portal.translate(msgid, domain='collective.contact.core')

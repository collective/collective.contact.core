# -*- coding: utf-8 -*-
from collective.contact.core import _
from Products.Five import BrowserView
from zope.i18n import translate

import json


class GenderPersonTitleMapping(BrowserView):

    """Return gender/person_title mapping in json."""

    def __call__(self):
        request = self.request
        request.response.setHeader(
            'Content-Type', 'application/json')
        return json.dumps({
            'M': translate(_(u"Mr"), context=request),
            'F': translate(_(u"Mrs"), context=request),
        })

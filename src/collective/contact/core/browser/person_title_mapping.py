# -*- coding: utf-8 -*-
import json

from five import grok
from zope.i18n import translate
from zope.interface import Interface

from collective.contact.core import _


class GenderPersonTitleMapping(grok.View):

    """Return gender/person_title mapping in json."""

    grok.name("gender_person_title_mapping.json")
    grok.context(Interface)
    grok.require('zope2.View')

    def render(self):
        request = self.request
        request.response.setHeader(
            'Content-Type', 'application/json')
        return json.dumps({
            'M': translate(_(u"Mr"), context=request),
            'F': translate(_(u"Mrs"), context=request),
        })

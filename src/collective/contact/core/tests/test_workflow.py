# -*- coding: utf8 -*-

import unittest2 as unittest

from ecreall.helpers.testing import member as memberhelpers
from ecreall.helpers.testing.workflow import BaseWorkflowTest

from collective.contact.core.testing import INTEGRATION


USERDEFS = [
        {'user': 'manager', 'roles': ('Manager', 'Member',), 'groups': ()},
        {'user': 'contributor', 'roles': ('Contributor', 'Member',), 'groups': ()},
        {'user': 'member', 'roles': ('Member',), 'groups': ()},
        ]


PERSON_PERMISSIONS = {'active':
                        {'Access contents information':
                         ('manager', 'contributor', 'member'),
                         'Modify portal content':
                         ('manager', 'contributor'),
                         'View':
                         ('manager', 'contributor', 'member'),
                        },
                     'deactivated':
                        {'Access contents information':
                         ('manager', 'contributor'),
                         'Modify portal content':
                         ('manager', 'contributor'),
                         'View':
                         ('manager', 'contributor'),
                        },
                     }


WORKFLOW_TRACK = [('', 'active'),
                  ('deactivate', 'deactivated'),
                  ('activate', 'active'),
                 ]


class TestSecurity(unittest.TestCase, BaseWorkflowTest):
    """Tests collective.contact.core workflows"""

    layer = INTEGRATION

    def setUp(self):
        super(TestSecurity, self).setUp()
        self.portal = self.layer['portal']
        memberhelpers.createMembers(self.portal, USERDEFS)
        self.mydirectory = self.portal['mydirectory']
        self.degaulle = self.mydirectory['degaulle']

    def test_person_permissions(self):
        degaulle = self.degaulle
        workflow = self.portal.portal_workflow
        self.login('manager')
        self.assertCheckPermissions(degaulle, PERSON_PERMISSIONS['active'], USERDEFS)

        for (transition, state) in WORKFLOW_TRACK:
            if transition:
                workflow.doActionFor(degaulle, transition)
            if state:
                self.assertHasState(degaulle, state)
                self.assertCheckPermissions(degaulle, PERSON_PERMISSIONS[state],
                                            USERDEFS, stateid=state)

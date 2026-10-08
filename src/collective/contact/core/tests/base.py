# -*- coding: utf8 -*-
"""Small test helpers (replacement for ecreall.helpers.testing)."""
from AccessControl import getSecurityManager
from plone import api
from plone.app.testing import login
from plone.app.testing import logout


class BaseTest(object):
    """Mixin for unittest.TestCase using a plone.app.testing layer."""

    def login(self, username):
        login(self.layer['portal'], username)

    def logout(self):
        logout()

    def getBrain(self, uid):
        brains = api.content.find(UID=uid)
        return brains[0] if brains else None


def create_members(portal, userdefs):
    for userdef in userdefs:
        username = userdef['user']
        api.user.create(
            email='{}@example.com'.format(username),
            username=username,
            password='secret_pass_123',
            roles=tuple(userdef['roles']),
        )
        for group in userdef.get('groups', ()):
            api.group.add_user(groupname=group, username=username)


class BaseWorkflowTest(BaseTest):

    def assertHasState(self, obj, state):
        self.assertEqual(api.content.get_state(obj), state)

    def assertCheckPermissions(self, obj, permissions, userdefs, stateid=None):
        """Check that for each permission, only the listed users have it."""
        for permission, allowed in permissions.items():
            for userdef in userdefs:
                username = userdef['user']
                self.login(username)
                has_perm = bool(getSecurityManager().checkPermission(permission, obj))
                self.assertEqual(
                    has_perm, username in allowed,
                    "{} permission {} for {}{}".format(
                        'Missing' if username in allowed else 'Unexpected',
                        permission, username,
                        ' in state {}'.format(stateid) if stateid else ''))
        self.login('manager')

from collective.contact.core.testing import COLLECTIVE_CONTACT_CORE_ACCEPTANCE_TESTING
from plone import api

import unittest


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_CONTACT_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        super(TestSetup, self).setUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = api.portal.get_tool('portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        self.assertTrue(self.qi_tool.isProductInstalled(
            'collective.contact.core'))

    def test_test_data_created(self):
        self.assertTrue('mydirectory' in self.portal)

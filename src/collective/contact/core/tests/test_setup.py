from collective.contact.core.testing import COLLECTIVE_CONTACT_CORE_ACCEPTANCE_TESTING
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_CONTACT_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        super(TestSetup, self).setUp()
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi = get_installer(self.portal)

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        self.assertTrue(self.qi.is_product_installed(
            'collective.contact.core'))

    def test_test_data_created(self):
        self.assertTrue('mydirectory' in self.portal)

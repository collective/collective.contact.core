from collective.contact.core.testing import INTEGRATION
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_is_installed(self):
        """Test if collective.contact.core is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.contact.core"))

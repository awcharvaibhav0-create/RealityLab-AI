import unittest


class TestNavigation(unittest.TestCase):
    def test_navigation_items(self):
        from frontend.navigation import get_navigation

        nav = get_navigation()
        self.assertIsInstance(nav, list)
        self.assertTrue(len(nav) > 0)

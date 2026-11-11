from django.test import SimpleTestCase
from django.urls import get_resolver


class UrlConfigurationTests(SimpleTestCase):
    def test_home_url_is_registered_only_once(self):
        home_patterns = [
            pattern for pattern in get_resolver().url_patterns
            if getattr(pattern, 'name', None) == 'home'
        ]

        self.assertEqual(len(home_patterns), 1)
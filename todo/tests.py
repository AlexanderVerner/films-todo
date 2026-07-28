from django.test import TestCase
from django.utils.safestring import SafeString
from todo.templatetags.todo_extras import format_watchability


class FormatWatchabilityTests(TestCase):
    """Test XSS prevention in format_watchability filter."""

    def test_valid_http_url(self):
        """Valid HTTP URL should be rendered as link."""
        sources = [{'url': 'http://example.com', 'name': 'Example'}]
        result = format_watchability(sources)
        self.assertIn('href="http://example.com"', result)
        self.assertIn('>Example</a>', result)
        self.assertIsInstance(result, SafeString)

    def test_valid_https_url(self):
        """Valid HTTPS URL should be rendered as link."""
        sources = [{'url': 'https://example.com', 'name': 'Example'}]
        result = format_watchability(sources)
        self.assertIn('href="https://example.com"', result)
        self.assertIn('>Example</a>', result)

    def test_javascript_url_blocked(self):
        """JavaScript URL should not create executable link."""
        sources = [{'url': "javascript:alert('XSS')", 'name': 'Bad Link'}]
        result = format_watchability(sources)
        self.assertNotIn('href="javascript', result)
        self.assertNotIn('alert', result)
        # Should output only the name without link
        self.assertIn('Bad Link', result)

    def test_data_url_blocked(self):
        """Data URL should not create executable link."""
        sources = [{'url': 'data:text/html,<script>alert("XSS")</script>', 'name': 'Data'}]
        result = format_watchability(sources)
        self.assertNotIn('href="data:', result)
        self.assertNotIn('<script>', result)
        self.assertIn('Data', result)

    def test_vbscript_url_blocked(self):
        """VBScript URL should be blocked."""
        sources = [{'url': 'vbscript:msgbox("XSS")', 'name': 'VB'}]
        result = format_watchability(sources)
        self.assertNotIn('href="vbscript', result)

    def test_multiple_sources_mixed(self):
        """Multiple sources with valid and invalid URLs."""
        sources = [
            {'url': 'https://example.com', 'name': 'Valid'},
            {'url': "javascript:alert('xss')", 'name': 'Invalid'},
            {'url': 'http://safe.com', 'name': 'Also Valid'},
        ]
        result = format_watchability(sources)
        # Valid links should be present
        self.assertIn('href="https://example.com"', result)
        self.assertIn('href="http://safe.com"', result)
        # Invalid link should not be present
        self.assertNotIn('javascript:', result)
        # But names should all be present
        self.assertIn('Valid', result)
        self.assertIn('Invalid', result)
        self.assertIn('Also Valid', result)

    def test_empty_sources(self):
        """Empty sources should return empty string."""
        self.assertEqual(format_watchability([]), '')
        self.assertEqual(format_watchability(None), '')

    def test_platform_fallback(self):
        """If no name provided, should use platform."""
        sources = [{'url': 'https://example.com', 'platform': 'Netflix'}]
        result = format_watchability(sources)
        self.assertIn('>Netflix</a>', result)

    def test_url_fallback_safe_scheme(self):
        """If no name/platform, use URL if scheme is safe."""
        sources = [{'url': 'https://example.com'}]
        result = format_watchability(sources)
        self.assertIn('https://example.com', result)

    def test_no_href_created_for_unsafe_scheme(self):
        """Ensure no href attribute is created for unsafe schemes."""
        sources = [{'url': 'file:///etc/passwd', 'name': 'File'}]
        result = format_watchability(sources)
        self.assertNotIn('href=', result)


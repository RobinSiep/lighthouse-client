from unittest import TestCase

from lighthouseclient.machine import shutdown


class TestShutdown(TestCase):
    def test_shutdown_success(self):
        status, error = shutdown()
        self.assertTrue(status)
        self.assertIs(error, None)

    def test_shutdown_insufficient_permissions(self):
        status, error = shutdown()
        self.assertFalse(status)
        self.assertIn("Insufficient permissions to perform shutdown", error)

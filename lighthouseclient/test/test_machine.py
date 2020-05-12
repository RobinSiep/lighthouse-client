from subprocess import PIPE
from unittest import TestCase
from unittest.mock import patch

from lighthouseclient.machine import shutdown


class TestShutdown(TestCase):
    def test_shutdown_success(self):
        with patch('lighthouseclient.machine.Popen') as MockedPopen:
            instance = MockedPopen.return_value
            instance.communicate.return_value = b"", None
            instance.returncode = 0

            status, error = shutdown()
            self.assertTrue(status)
            self.assertIs(error, None)
            MockedPopen.assert_called_with(
                ('shutdown', '-h', 'now'), stdout=PIPE, stderr=PIPE
            )

    def test_shutdown_insufficient_permissions(self):
        with patch('lighthouseclient.machine.Popen') as MockedPopen:
            instance = MockedPopen.return_value
            instance.communicate.return_value = b"", b"NOT super-user"
            instance.returncode = -1

            status, error = shutdown()
            self.assertFalse(status)
            self.assertIn(
                "Insufficient permissions to perform shutdown", error
            )
            MockedPopen.assert_called_with(
                ('shutdown', '-h', 'now'), stdout=PIPE, stderr=PIPE
            )

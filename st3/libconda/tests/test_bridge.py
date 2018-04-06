import unittest
from unittest.mock import patch, Mock


class TestGolcondaBridge(unittest.TestCase):
    """Tests GolcondaBridge class
    """

    def setUp(self):
        self.requests = Mock()
        self.requests.post.return_value = 200

    def test_bridge(self):
        with patch.dict('sys.modules', requests=self.requests):
            from libconda.bridge import GolcondaBridge

            sut = GolcondaBridge('localhost', 19360)
            self.assertEqual(sut.hostname, 'http://localhost:19360')

            got = sut.request('test', {})
            self.assertEqual(got, 200)
            self.requests.post.assert_called_once_with(
                'http://localhost:19360/test', json={}, timeout=0.1
            )

import bencode
import unittest


class DecodeTests(unittest.TestCase):

    def test_int(self):
        self.assertEqual(123, bencode.decode('i123e'))

    def test_str(self):
        self.assertEqual('abc', bencode.decode('3:abc'))

    def test_list(self):
        self.assertEqual([1, '2', 3], bencode.decode('li1e1:2i3ee'))

import bencode
import unittest


class DecodeTests(unittest.TestCase):

    def test_int(self):
        self.assertEqual(123, bencode.decode('i123e'))

    def test_str(self):
        self.assertEqual('abc', bencode.decode('3:abc'))

    def test_list(self):
        self.assertEqual([1, '2', 3], bencode.decode('li1e1:2i3ee'))

    def test_dict(self):
        self.assertEqual({'1': 1, '2': 2}, bencode.decode('d1:1i1e1:2i2ee'))


class EncodeTests(unittest.TestCase):

    def test_int(self):
        self.assertEqual('i123e', bencode.encode(123))

    def test_str(self):
        self.assertEqual('3:abc', bencode.encode('abc'))

    def test_list(self):
        self.assertEqual('li1ei2ei3ee', bencode.encode([1, 2, 3]))

    def test_dict(self):
        # testing with only one key because dict object does not have a key
        # order which makes it hard to test multiple keys.
        self.assertEqual('d1:1i1ee',
                         bencode.encode({'1': 1}))


class InverseFunctionTests(unittest.TestCase):

    def test_dict(self):
        obj = {'list_int': [1, 2, [1, 2]],
               'list_str': ['11', '22', '33'],
               'num': 12345,
               'str': 'str',
               'dict': {'1': 1, '2': 2}}
        self.assertEqual(obj, bencode.decode(bencode.encode(obj)))

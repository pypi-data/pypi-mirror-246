import unittest
from parameterized import parameterized
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.peripherals.eeeprom.requests.read import ReadRequest


class ReadRequestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dpa = b'\x05\x00\x04\x02\xff\xff\x0a\x00\x05'
        self.json = {
            'mType': 'iqrfEmbedEeeprom_Read',
            'data': {
                'msgId': 'readTest',
                'req': {
                    'nAdr': 5,
                    'hwpId': 65535,
                    'param': {
                        'address': 10,
                        'len': 5
                    }
                },
                'returnVerbose': True
            }
        }

    @parameterized.expand([
        [5, 10, 5, b'\x05\x00\x04\x02\xff\xff\x0a\x00\x05'],
        [0, 5, 22, b'\x00\x00\x04\x02\xff\xff\x05\x00\x16'],
        [5, 65535, 10, b'\x05\x00\x04\x02\xff\xff\xff\xff\x0a']
    ])
    def test_to_dpa(self, nadr: int, address: int, length: int, expected):
        request = ReadRequest(nadr=nadr, address=address, length=length)
        self.assertEqual(
            request.to_dpa(),
            expected
        )

    @parameterized.expand([
        [5, 10, 5],
        [0, 5, 22],
        [5, 12345, 20]
    ])
    def test_to_json(self, nadr: int, address: int, length: int):
        request = ReadRequest(nadr=nadr, address=address, length=length, msgid='readTest')
        self.json['data']['req']['nAdr'] = nadr
        self.json['data']['req']['param']['address'] = address
        self.json['data']['req']['param']['len'] = length
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [2, b'\x05\x00\x04\x02\xff\xff\x02\x00\x05'],
        [17, b'\x05\x00\x04\x02\xff\xff\x11\x00\x05'],
        [65534, b'\x05\x00\x04\x02\xff\xff\xfe\xff\x05'],
    ])
    def test_set_address(self, address, dpa):
        request = ReadRequest(nadr=5, address=10, length=5, msgid='readTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.address = address
        self.json['data']['req']['param']['address'] = address
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [20, b'\x05\x00\x04\x02\xff\xff\x0a\x00\x14'],
        [13, b'\x05\x00\x04\x02\xff\xff\x0a\x00\x0d'],
    ])
    def test_set_length(self, length, dpa):
        request = ReadRequest(nadr=5, address=10, length=5, msgid='readTest')
        self.assertEqual(
            request.to_dpa(),
            self.dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )
        request.length = length
        self.json['data']['req']['param']['len'] = length
        self.assertEqual(
            request.to_dpa(),
            dpa
        )
        self.assertEqual(
            request.to_json(),
            self.json
        )

    @parameterized.expand([
        [-1],
        [65536],
        [100000]
    ])
    def test_set_address_invalid(self, address):
        request = ReadRequest(nadr=5, address=10, length=5, msgid='readTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.address = address

    @parameterized.expand([
        [-1],
        [256],
        [1000]
    ])
    def test_set_length_invalid(self, length):
        request = ReadRequest(nadr=5, address=10, length=5, msgid='readTest')
        with self.assertRaises(RequestParameterInvalidValueError):
            request.length = length

    @parameterized.expand([
        [-1, 1],
        [65536, 10],
        [100000, 15],
        [10, -1],
        [10, 256]
    ])
    def test_construct_invalid(self, address, length):
        with self.assertRaises(RequestParameterInvalidValueError):
            ReadRequest(nadr=0, address=address, length=length)

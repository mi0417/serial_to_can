import unittest
from common_data_utils import hex_str_to_little_endian_array, little_endian_array_to_hex_str, ascii_to_little_endian_array, little_endian_array_to_ascii

class TestHexStrToLittleEndianArray(unittest.TestCase):

    def test_valid_hex_str(self):
        # 测试有效的十六进制字符串
        hex_str = '1234567890abcdef'
        expected_result = b'\xef\xcd\xab\x90\x78\x56\x34\x12'
        self.assertEqual(hex_str_to_little_endian_array(hex_str), expected_result)

    def test_hex_str_with_0x_prefix(self):
        # 测试带有 '0x' 前缀的十六进制字符串
        hex_str = '0x1234567890abcdef'
        expected_result = b'\xef\xcd\xab\x90\x78\x56\x34\x12'
        self.assertEqual(hex_str_to_little_endian_array(hex_str), expected_result)

    def test_empty_hex_str(self):
        # 测试空的十六进制字符串
        hex_str = ''
        expected_result = b''
        self.assertEqual(hex_str_to_little_endian_array(hex_str), expected_result)

    def test_invalid_hex_str(self):
        hex_str = '1234567G'
        result = hex_str_to_little_endian_array(hex_str)
        self.assertEqual(result, None)

    def test_valid_byte_array(self):
        # 测试有效的小端字节数组
        byte_array = b'\x78\x56\x34\x12'
        expected_hex_str = '12345678'
        self.assertEqual(little_endian_array_to_hex_str(byte_array), expected_hex_str)

    def test_invalid_type(self):
        # 测试无效的类型
        invalid_array = 123
        self.assertIsNone(little_endian_array_to_hex_str(invalid_array))

    def test_empty_string(self):
        # 测试空字符串
        result = ascii_to_little_endian_array('')
        self.assertEqual(result, b'')

    def test_single_character(self):
        # 测试单个字符
        result = ascii_to_little_endian_array('A')
        self.assertEqual(result, b'A')

    def test_multiple_characters(self):
        # 测试多个字符
        result = ascii_to_little_endian_array('ABC')
        self.assertEqual(result, b'CBA')


if __name__ == '__main__':
    unittest.main()

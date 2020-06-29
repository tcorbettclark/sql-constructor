import unittest

from sqlcon import is_invalid_name, make_valid_name


class TestMakeValidName(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(make_valid_name(""), "")

    def test_already_valid(self):
        self.assertEqual(make_valid_name("abc"), "abc")
        self.assertEqual(make_valid_name("aBc"), "aBc")
        self.assertEqual(make_valid_name("ABc"), "ABc")
        self.assertEqual(make_valid_name("ABc123"), "ABc123")
        self.assertEqual(make_valid_name("ABc_123"), "ABc_123")

    def test_numbers(self):
        self.assertEqual(make_valid_name("12abc"), "abc")
        self.assertEqual(make_valid_name("012abc"), "abc")
        self.assertEqual(make_valid_name("012abc345"), "abc345")

    def test_hypens(self):
        self.assertEqual(make_valid_name("ABc-123"), "ABc_123")
        self.assertEqual(make_valid_name("-ABc-123"), "_ABc_123")
        self.assertEqual(make_valid_name("-ABc-123-"), "_ABc_123_")

    def test_spaces(self):
        self.assertEqual(make_valid_name("abc def"), "abc_def")
        self.assertEqual(make_valid_name("  abc def"), "__abc_def")
        self.assertEqual(make_valid_name("  abc def "), "__abc_def_")

    def test_newlines(self):
        self.assertEqual(make_valid_name("abc\ndef"), "abcdef")
        self.assertEqual(make_valid_name("\n\nabc\ndef"), "abcdef")
        self.assertEqual(make_valid_name("\n\nabc\ndef\n"), "abcdef")


class TestIsInvalidName(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(is_invalid_name(""))

    def test_valid_names(self):
        self.assertFalse(is_invalid_name("abc123"))
        self.assertFalse(is_invalid_name("A2b3C"))
        self.assertFalse(is_invalid_name("_A"))
        self.assertFalse(is_invalid_name("_"))
        self.assertFalse(is_invalid_name("abc_123"))

    def test_hypens(self):
        self.assertTrue(is_invalid_name("abc-123"))
        self.assertTrue(is_invalid_name("abc-"))
        self.assertTrue(is_invalid_name("-abc"))

    def test_leading_numbers(self):
        self.assertTrue(is_invalid_name("123abc"))

    def test_whitespace(self):
        self.assertTrue(is_invalid_name("abc def"))
        self.assertTrue(is_invalid_name("abc\ndef"))

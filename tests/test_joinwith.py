import unittest

import sqlcon


class TestJoinWith(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(sqlcon.joinwith([]), [])

    def test_one(self):
        self.assertEqual(sqlcon.joinwith(["a"]), ["a"])

    def test_one_with_newlines(self):
        self.assertEqual(sqlcon.joinwith(["a\n"]), ["a"])
        self.assertEqual(sqlcon.joinwith(["\na"]), ["a"])
        self.assertEqual(sqlcon.joinwith(["\na\n"]), ["a"])

    def test_one_with_include_last(self):
        self.assertEqual(sqlcon.joinwith(["a"], include_last=True), ["a,"])

    def test_one_with_include_last_with_newlines(self):
        self.assertEqual(sqlcon.joinwith(["a\n"], include_last=True), ["a,"])
        self.assertEqual(sqlcon.joinwith(["\na"], include_last=True), ["a,"])
        self.assertEqual(sqlcon.joinwith(["\na\n"], include_last=True), ["a,"])

    def test_use_different_separator(self):
        self.assertEqual(
            sqlcon.joinwith(["a", "b"], separator="-BOO-"), ["a-BOO-", "b"]
        )
        self.assertEqual(
            sqlcon.joinwith(["a", "b"], separator="-BOO-", include_last=True),
            ["a-BOO-", "b-BOO-"],
        )

    def test_composite(self):
        self.assertEqual(
            sqlcon.joinwith([["a", "b"], ["c"], "d", "e"]),
            [["a", "b,"], ["c,"], "d,", "e"],
        )

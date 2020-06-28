import unittest

import sqlcon


class TestProcess(unittest.TestCase):
    def test_degenerate_empty_list(self):
        self.assertEqual(sqlcon.process([]), "")

    def test_degenerate_empty_tuple(self):
        self.assertEqual(sqlcon.process(()), "")

    def test_degenerate_indent_only(self):
        self.assertEqual(sqlcon.process([1]), "")

    def test_plain_text(self):
        self.assertEqual(sqlcon.process(["foo"]), "foo\n")

    def test_plain_text_multiline(self):
        def f():
            yield """
                foo
            """

        self.assertEqual(sqlcon.process(f()), "foo\n")

    def test_plain_text_indent(self):
        def f():
            yield """
                foo
                    bar
                foo
            """
            yield """
                foo
            """

        self.assertEqual(sqlcon.process(f()), "foo\n    bar\nfoo\nfoo\n")

    def test_mixed_text_and_indents(self):
        def f():
            yield """
                foo
            """
            yield 1, "bar", -1
            yield "foo"

        self.assertEqual(sqlcon.process(f()), "foo\n    bar\nfoo\n")

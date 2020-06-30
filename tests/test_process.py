import io
import os
import pathlib
import sys
import tempfile
import unittest

import sqlcon


class TestProcess(unittest.TestCase):
    def test_degenerate_empty_string(self):
        self.assertEqual(sqlcon.process(""), "\n")

    def test_degenerate_empty_list(self):
        self.assertEqual(sqlcon.process([]), "")

    def test_degenerate_empty_tuple(self):
        self.assertEqual(sqlcon.process(()), "")

    def test_degenerate_indent_only(self):
        self.assertEqual(sqlcon.process([1]), "")

    def test_empty_text(self):
        self.assertEqual(sqlcon.process([""]), "\n")

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


class TestProcessWrite(unittest.TestCase):
    def test_write_to_sysout(self):
        temp = sys.stdout
        try:
            sys.stdout = io.StringIO()
            sqlcon.process("foo", output="stdout")
            self.assertEqual(sys.stdout.getvalue(), "foo\n")
        finally:
            sys.stdout = temp

    def test_write_to_path(self):
        fd, filename = tempfile.mkstemp()
        os.close(fd)
        p = pathlib.Path(filename)
        try:
            sqlcon.process("foo", output=p)
            self.assertEqual(p.read_text(), "foo\n")
        finally:
            p.unlink()

    def test_write_to_file(self):
        fd, filename = tempfile.mkstemp()
        os.close(fd)
        try:
            sqlcon.process("foo", output=filename)
            self.assertEqual(open(filename).read(), "foo\n")
        finally:
            os.unlink(filename)

    def test_write_to_file_like_object(self):
        output = io.StringIO()
        sqlcon.process("foo", output=output)
        self.assertEqual(output.getvalue(), "foo\n")

    def test_write_to_unwritable_object(self):
        with self.assertRaises(ValueError):
            sqlcon.process("foo", output=object())

import unittest

import sqlcon

sq = sqlcon.single_quote
dq = sqlcon.double_quote


def select_columns(variables):
    yield sqlcon.joinwith(dq(v) for v in variables)


def subquery():
    yield """
        SELECT
            *
        FROM
            some_table
        LEFT JOIN
            some_other_table
        USING
            some_table.id = some_other_table.key
    """, -1


def where_clause(variables, condition):
    variable, comparator, constant = condition
    assert variable in variables, f"Unknown variable: {variable}"
    assert comparator == "=", f"Unknown comparator: {comparator}"
    yield f"{dq(variable)} = {sq(constant)}"


def example(variables, condition):
    yield """
        SELECT
    """
    yield 1, select_columns(variables), -1
    yield """
        FROM
            (
    """
    yield 1, subquery(), -1
    yield """
            ) AS tmp
        WHERE
    """, 1
    yield where_clause(variables, condition)


class TestExample1(unittest.TestCase):
    def test_example1(self):
        sql = example(["name", "address"], ("name", "=", "tim"))
        self.assertEqual(
            sqlcon.process(sql),
            """SELECT
    "name",
    "address"
FROM
    (
        SELECT
            *
        FROM
            some_table
        LEFT JOIN
            some_other_table
        USING
            some_table.id = some_other_table.key
    ) AS tmp
WHERE
    "name" = 'tim'
""",
        )

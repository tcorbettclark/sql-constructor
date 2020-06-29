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


def where_clauses(variables, conditions):
    for condition in conditions:
        variable, comparator, constant = condition
        assert variable in variables, f"Unknown variable: {variable}"
        assert comparator in ("=", "~"), f"Unknown comparator: {comparator}"
        yield f"{dq(variable)} {comparator} {sq(constant)}"


def example(variables, conditions):
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
    """
    yield sqlcon.indented_joinwith(
        where_clauses(variables, conditions), separator=" AND "
    )


class TestExample1(unittest.TestCase):
    def test_example1(self):
        sql = example(
            ["name", "age", "address"],
            [("name", "=", "tim"), ("address", "~", "England")],
        )
        self.assertEqual(
            sqlcon.process(sql),
            """SELECT
    "name",
    "age",
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
    "name" = 'tim' AND
    "address" ~ 'England'
""",
        )

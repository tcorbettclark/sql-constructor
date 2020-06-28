![Tests](https://github.com/tcorbettclark/sql-constructor/workflows/Continuous%20Integration%20tests%20etc/badge.svg)

[![Known Vulnerabilities from Snyk](https://snyk.io/test/github/tcorbettclark/sql-constructor/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/tcorbettclark/sql-constructor?targetFile=requirements.txt)

# sql-constructor

Programming approach and utility functions to construct and maintain
well-formatted SQL from Python 3.6 and above.

## Motivation and Philosophy

Like all programming languages, the task of writing maintainable SQL is made a
little bit easier through good formatting and layout, reducing the cognitive
load. Doing this with completely static SQL is possible e.g. with static
formatters, but much harder to achieve when *programmatically* constructing the
SQL. In my experience one easily looses the formating in *both* the generating
Python code *and* in the generated SQL. Ouch.

This package aims to solve this problem with a particular programming pattern
and a small number of utility functions.

In particular, the objectives are:

* To have the SQL look as much like SQL within the source Python code whilst
  still using obvious Python to generate it. Obviously this involves trade-offs.
* To have the generated SQL look like it could have been written directly, so
  that it can be read and understood as easily as possible.
* To be able to write optimum SQL *in SQL*, rather than trying to write optimum
  SQL from another language but mentally thinking in the target SQL.

It should be clear that **SQL-Constructor** is not an ORM. There is no abstraction.
In fact, quite the opposite.

## SQL variants

This library has been used to generate SQL for PostgreSQL. However it should
work with other database engines / language variants with little or no change.
Similarly, it is agnostic to SQL code style conventions because that's
controlled by the programmer.

In fact the whole idea is not really about SQL at all, but about managing text.

## Example

Some examples will illustrate the approach.

```python
import sqlcon

sq = sqlcon.single_quote
dq = sqlcon.double_quote


def select_columns(variables):
    yield sqlcon.indented_joinwith(dq(v) for v in variables)


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
    yield select_columns(variables)
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


if __name__ == "__main__":
    sql = example(["name", "address"], ("name", "=", "tim"))
    print(sqlcon.process(sql))

```

This produces:

```sql
SELECT
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
```

Some relatively subtle things are happening automatically:

1. Common indentation is being removed to left align the base of the generated SQL.
1. Blank lines are being stripped intelligently. E.g. the start and end of the
   tripple quoted sql strings.
1. The indentation levels are being tracked. E.g. note how the subquery is
   indented in the output, but not in the input `subqery()` function.
1. The processing takes strings (for the actual SQL), integers (for manual
   indentation changes), and lists/tuples/generators for composition of the
   above.

## Library functions

TODO


# Release checklist

* Run: `black .`
* Run: `isort`
* Run: `flake8 .`
* Run: `nose2 -v tests`
* Run: `poetry export -f requirements.txt >requirements.txt` (for snyk scanning)
* Ensure `git tag`, the package version (via `poetry version`), and `sqlcon.__version__` are all equal!
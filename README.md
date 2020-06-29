![Tests on 3.6, 3.7, 3.8](https://github.com/tcorbettclark/sql-constructor/workflows/Tests/badge.svg) [![Known Vulnerabilities from Snyk](https://snyk.io/test/github/tcorbettclark/sql-constructor/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/tcorbettclark/sql-constructor?targetFile=requirements.txt)

# SQL Constructor

A programming approach (and supporting functions) to programmatically construct
and maintain well-formatted SQL from Python 3.6 and above.

## Motivation and Philosophy

Like all programming languages, the task of writing maintainable SQL is made a
little bit easier through good formatting and layout, reducing the cognitive
load on the programmers. Doing this with completely static SQL is possible e.g.
with static formatters, but is harder to achieve when *programmatically*
constructing the SQL. In my experience one easily looses the formating in *both*
the generating Python code *and* in the generated SQL. Ouch.

This package aims to solve this problem with a particular programming pattern
and a small number of utility functions.

In particular, the objectives are:

* To have the SQL look as much like SQL within the source Python code whilst
  still using obvious Python to generate it. This involves trade-offs.
* To have the generated SQL look like it could have been written directly so
  that it can be read and understood as easily as possible.
* To be able to write optimum SQL *in SQL* rather than trying to write optimum
  SQL from another language but mentally thinking in the target SQL.

It should be clear that **SQL Constructor** is not an ORM. There is no abstraction.
In fact, quite the opposite.

## SQL variants

This library has been used to generate SQL for PostgreSQL. However it should
work with other database engines / language variants with little or no change.
Similarly, it is agnostic to SQL code style conventions because that is
controlled by the programmer.

In fact the whole idea is not really about SQL at all, but about managing text.

## Example

A simple example will illustrate the approach. From the perspective of SQL the
subquery is unnecessary; it is used purely to show composition.

```python
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


if __name__ == "__main__":
    sql = example(
        ["name", "age", "address"],
        [("name", "=", "tim"), ("address", "~", "England")],
    )
    print(sqlcon.process(sql))

```

When run, this produces:

```sql
SELECT
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
```

The processing takes strings (for the actual SQL), integers (for manual
indentation changes), and lists/tuples/generators for composition of the above.
Clearly this example is rather degenerate. It also mixes a few styles which is
inconsistent but illustrates a few different approaches.

Note how some relatively subtle things are happening automatically:

1. Common indentation is being removed to left align the base of the generated SQL.
1. Blank lines are being stripped intelligently. E.g. the start and end of the
   tripple quoted strings.
1. The indentation levels are being tracked. E.g. the subquery is indented in
   the output but not in the `subquery()` function. So nested layers (such as
   views within views or views within PostgreSQL functions) can be written
   neatly without worrying about the indentation of their containing scope.

## API

The **SQL Constructor** API consists of the following functions:

* `process` to convert the SQL strings, indentation integers, and composition of
  these as iterables all into output SQL.
* `single_quote` to correctly quote literal strings for PostgreSQL.
* `double_quote` to correctly quote identifiers for PostgresSQL.
* `joinwith` to join lists with commas (e.g. for lists of column identifers or
  "IN" clauses) or conditions with "AND" (e.g. for conjunctions in WHERE clauses).
  Can be used either on a single line or across multiple lines with maintained
  indentation.
* `indented_joinwith` as a shorthand to prefix `joinwth` with an indent and
  postfix with an outdent.

See the source code docstrings for details.

## Tests

See the unittests in the `tests/` directory.

# Alternatives

Before deciding to create **SQL Constructor** I tried various approaches "in
anger" on real projects. Most notably:

* Templating the SQL either with vanilla Jinja2 or variants designed to work
  with SQL like JinjaSQL (e.g. https://github.com/hashedin/jinjasql).
  Maintaining formatting is difficult, and now you are working in 2 files
  (Python and the template) and 3 languages (templating, Python, and SQL).

* Using an ORM like SQLAlchemy. Whilst superficially clean ("it's all just
  Python"), anything more than the most trivial quickly requires mental
  gymnastics *thinking* in SQL but *writing* in Python, and needing to drop out
  of the Python API to create separate SQL support functions and views etc in
  order to get the most from the database engine.

Neither of these worked for me.

# Contributions

I'd love to hear of other approaches people have tried. Perhaps there is a
better way?! Similarly, pull-requests and bug reports etc are all welcome.

# Release checklist

* Run: `black .`
* Run: `isort -y`
* Run: `flake8 .`
* Run: `nose2 -v tests`
* Run: `poetry export -f requirements.txt >requirements.txt` (for snyk scanning)
* Ensure `git tag`, the package version (via `poetry version`), and `sqlcon.__version__` are all equal!
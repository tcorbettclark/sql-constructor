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

* To have the SQL look as much like SQL within the source Python code.
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

TODO

If that looks like nothing much is happening then good! A few subtle things are
happening though:

1. Blank lines are being stripped intelligently.
1. The indentation levels are being tracked.
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
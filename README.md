![Continuous Integration tests etc](https://github.com/tcorbettclark/sql-constructor/workflows/Continuous%20Integration%20tests%20etc/badge.svg)

[![Known Vulnerabilities](https://snyk.io/test/github/tcorbettclark/sql-constructor/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/tcorbettclark/sql-constructor?targetFile=requirements.txt)

# sql-constructor

Convenient functions and approach for constructing indented SQL from Python.

## Motivation

Like all programming languages, the task of writing good SQL is made a little
bit easier by good formatting and layout - reducing the cognitive load. Doing
this with completely static SQL is possible e.g. with static formatters, but
much harder to achieve when programmatically constructing the SQL. In my
experience one looses the formmating in *both* the generating Python code *and*
in the generated SQL. Ouch.

This package aims to solve this problem with a particular programming pattern
and a small number of utility functions.

## SQL variants

This has only been used to generate SQL for PostgreSQL, although it should work
with other database engines / language variants with little or no change. In
fact the whole idea is not really about SQL at all, but about generating
indented text.

## Examples

TODO

```
```

## Library functions

TODO


# Release checklist

* Run: `black .`
* Run: `isort`
* Run: `flake8 .`
* Run: `nose2 -v`
* Run: `poetry export -f requirements.txt >requirements.txt` (for snyk scanning)
* Ensure `git tag`, the package version (via `poetry version`), and `sqlcon.__version__` are all equal!
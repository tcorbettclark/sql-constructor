# sql-constructor

Convenient functions and approach for constructing indented SQL from Python.

## Motivation

It is hard enough writing good SQL. Like all programming languages, the task is
made a little bit easier by good formatting and layout - reducing the cognitive
load. Doing this with completely static SQL is possible e.g. with static
formatters, but much harder to achieve when programmatically constructing the
SQL. In my experience one looses the formmating in *both* the generating Python
code *and* in the generated SQL. Ouch.

This package aims to solve this problem with a particular programming pattern
and a small number of utility functions.

## SQL variants

This has only been used to generate SQL for PostgreSQL, although it should work
with other database engines / language variants with little or no change. In
fact the whole idea is really only about indented text and not SQL at all.

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
* Ensure `git tag`, the package version (via `poetry version`), and `sqlcon.__version__` are all equal!
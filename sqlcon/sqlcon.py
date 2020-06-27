import sys

__all__ = ["process", "joinwith", "indented_joinwith"]


def _get_n_leading_spaces(line):
    """Return number of spaces before the first non-space character."""
    return len(line) - len(line.lstrip(" "))


def _strip(a):
    a = a.rstrip(" ")
    if a and a[0] == "\n":
        a = a[1:]
    if a and a[-1] == "\n":
        a = a[:-1]
    return a


def process(sqlcons, output_file=None, i=0, spaces="    "):
    """Process "sqlcons" into SQL written to given file object."""
    if output_file is None:
        output_file = sys.stdout
    # Use an inner function for recursive calling in a closure.
    def f(sqlcons):
        nonlocal i
        for s in sqlcons:
            if isinstance(s, str):
                lines = _strip(s).splitlines()
                if len(lines) > 0:
                    first_line_lead = _get_n_leading_spaces(lines[0])
                    for line in lines:
                        line = line.rstrip()
                        if line:
                            line = (i * spaces + line)[first_line_lead:]
                            output_file.write(line)
                        output_file.write("\n")
                    i = _get_n_leading_spaces(line) // len(spaces)
                else:
                    output_file.write("\n")
            elif isinstance(s, int):
                i += s
            else:
                # Assume some kind of iterable - list, tuple, or generator
                f(s)

    f(sqlcons)


def _add_trailing(thing, trailing_text):
    if isinstance(thing, str):
        return _strip(thing) + trailing_text
    things = list(thing)
    if len(things) > 0:
        things[-1] = _add_trailing(things[-1], trailing_text)
    return things


def joinwith(a_list, include_last=False, separator=","):
    """Return new sqlcons list joined with commas at end of all text items except for the last.

    Optionally use a different separator or include the separator on the last item too

    """
    a_list = list(a_list)
    if include_last:
        return [_add_trailing(a, separator) for a in a_list]
    else:
        if len(a_list) > 0:
            return [_add_trailing(a, separator) for a in a_list[:-1]] + [a_list[-1]]
        else:
            return []


def indented_joinwith(a_list, include_last=False, separator=","):
    """Same as `joinwith` but prepended with an indent and appended with an outdent."""
    return 1, joinwith(a_list, include_last=include_last, separator=separator), -1

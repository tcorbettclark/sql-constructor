import sqlcon


def abstract_example():
    yield """
        level 0
            level 1
                level 2
    """
    yield """
                level 2
            level 1
    """
    yield """
            level 1
    """, -1
    yield """
        level 0
            level 1
    """
    yield 1, sqlcon.joinwith(["level 2 - fred", "level 2 - alice", "level 2 - bob"])
    yield -3
    yield """
        level 0
    """


if __name__ == "__main__":
    sqlcon.process(abstract_example())

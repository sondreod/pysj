def task_format():
    return {
        "actions": ["black .", "isort ."],
        "verbosity": 2,
    }


def task_test():
    return {
        "actions": ["tox -e py39"],
        "verbosity": 2,
    }


def task_fulltest():
    return {
        "actions": ["tox --skip-missing-interpreters"],
        "verbosity": 2,
    }


def task_build():
    return {
        "actions": ["flit build"],
        "task_dep": ["precommit"],
        "verbosity": 2,
    }


def task_publish():
    return {
        "actions": ["flit publish"],
        "task_dep": ["build"],
        "verbosity": 2,
    }


def task_precommit():
    return {"actions": None, "task_dep": ["format", "fulltest"]}

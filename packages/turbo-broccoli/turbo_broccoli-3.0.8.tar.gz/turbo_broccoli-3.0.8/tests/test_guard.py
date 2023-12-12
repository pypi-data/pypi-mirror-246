# pylint: disable=missing-function-docstring
"""Test suite for guarded blocks/loops"""

from pathlib import Path

# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel

# Must be before turbo_broccoli imports
import common

from turbo_broccoli import (
    GuardedBlockHandler,
    guarded_call,
    produces_document,
    load_json,
)

TEST_PATH = Path("out") / "test"


def test_guarded_bloc_handler_iter():
    path = TEST_PATH / "test_guarded_bloc_handler_iter"
    h = GuardedBlockHandler(path)
    l1, l2 = [1, 2, 3], [2, 3, 4]
    # First loop
    for x in h.guard(l1):
        # Initialization of results at each iteration
        assert x in h.result
        assert h.result[x] is None
        h.result[x] = int(x)
    # Second loop over same iterable should be skipped
    for x in h.guard(l1):
        assert False
    # Final value
    assert h.result == {i: i for i in l1}
    # Check output files individually
    for x in l1:
        p = path / f"{x}.json"
        assert p.is_file()
        assert load_json(p) == int(x)
    # Second iteration where some output files already exist
    for x in h.guard(l2):
        if (
            int(x) <= 3
        ):  # Iterations for files that already exist should be skipped
            assert False
        h.result[x] = int(x)
    assert h.result == {i: i for i in l2}


def test_guarded_bloc_handler_no_iter():
    path = TEST_PATH / "test_guarded_bloc_handler_no_iter.json"
    h = GuardedBlockHandler(path)
    for _ in h.guard():
        h.result = 41
        h.result = 42
    # Block should be skipped
    for _ in h.guard():
        assert False
    assert h.result == 42
    assert h.result == load_json(path)


def test_guarded_bloc_handler_no_iter_native():
    import pandas as pd

    path = TEST_PATH / "test_guarded_bloc_handler_no_iter_native.csv"
    h = GuardedBlockHandler(path)
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": [1.0, 2.0, 3.0]})
    for _ in h.guard():
        h.result = df1
    for _ in h.guard():  # Block should be skipped
        assert False
    df2 = pd.read_csv(path)
    if "Unnamed: 0" in df2.columns:
        df2.drop(["Unnamed: 0"], axis=1, inplace=True)
    assert (df1 == df2).all().all()


def test_guarded_call():
    def f(a: int):
        return {"a": a}

    path = TEST_PATH / "test_guarded_call.json"
    x = guarded_call(f, path, 1)
    y = load_json(path)
    assert isinstance(x, dict)
    assert x == y
    assert x != f(2)
    assert x == guarded_call(f, path, 2)  # Intended behavior


def test_produces_document():
    def f(a: int):
        return {"a": a}

    path = TEST_PATH / "test_produces_document.json"
    _f = produces_document(f, path, check_args=False)
    x = _f(1)
    y = load_json(path)
    assert isinstance(x, dict)
    assert x == y
    assert x != f(2)
    assert x == _f(2)  # Intended behavior


def test_produces_document_check_args():
    def f(a: int):
        return {"a": a}

    path = TEST_PATH / "test_produces_document_check_args.json"
    _f = produces_document(f, path, check_args=True)
    assert _f(1) == {"a": 1}
    assert _f(2) == {"a": 2}
    assert _f(1) == {"a": 1}  # Repetition intended
    assert _f(2) == {"a": 2}  # Repetition intended
    assert _f(1) != _f(2)

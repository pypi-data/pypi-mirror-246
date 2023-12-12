"""
numpy (de)serialization utilities.

Todo:
    Handle numpy's `generic` type (which supersedes the `number` type).
"""
__docformat__ = "google"

import pickle
from typing import Any, Callable, Tuple
from uuid import uuid4

import numpy as np

try:
    from safetensors import numpy as st

    HAS_SAFETENSORS = True
except ModuleNotFoundError:
    HAS_SAFETENSORS = False
    from turbo_broccoli.utils import warn_about_safetensors

    warn_about_safetensors()


from turbo_broccoli.environment import (
    get_artifact_path,
    get_max_nbytes,
)
from turbo_broccoli.utils import (
    DeserializationError,
    TypeNotSupported,
    raise_if_nodecode,
)


def _json_to_dtype(dct: dict) -> np.dtype:
    """
    Converts a JSON document to a numpy dtype. See `to_json` for the
    specification `dct` is expected to follow. Note that the key `__numpy__`
    should not be present.
    """
    DECODERS = {
        1: _json_to_dtype_v1,
    }
    return DECODERS[dct["__version__"]](dct)


def _json_to_dtype_v1(dct: dict) -> np.dtype:
    """
    Converts a JSON document to a numpy dtype object following the v1
    specification.
    """
    return np.lib.format.descr_to_dtype(dct["dtype"])


def _json_to_ndarray(dct: dict) -> np.ndarray:
    """
    Converts a JSON document to a numpy array. See `to_json` for the
    specification `dct` is expected to follow. Note that the key `__numpy__`
    should not be present.
    """
    DECODERS = {
        1: _json_to_ndarray_v1,
        2: _json_to_ndarray_v2,
        3: _json_to_ndarray_v3,
    }
    return DECODERS[dct["__version__"]](dct)


def _json_to_ndarray_v1(dct: dict) -> np.ndarray:
    """
    Converts a JSON document to a numpy array following the v1 specification.
    """
    return np.frombuffer(
        dct["data"],
        dtype=np.lib.format.descr_to_dtype(dct["dtype"]),
    ).reshape(dct["shape"])


def _json_to_ndarray_v2(dct: dict) -> np.ndarray:
    """
    Converts a JSON document to a numpy array following the v1 specification.
    """
    if "data" in dct:
        return _json_to_ndarray_v1(dct)
    return np.load(get_artifact_path() / (dct["id"] + ".npy"))


def _json_to_ndarray_v3(dct: dict) -> np.ndarray:
    """
    Converts a JSON document to a numpy array following the v1 specification.
    """
    if not HAS_SAFETENSORS:
        raise RuntimeError(
            "A v3 numpy array document cannot be deserialized without "
            "safetensors. Install safetensors using "
            "'pip install safetensors'"
        )
    if "data" in dct:
        return st.load(dct["data"])["data"]
    return st.load_file(get_artifact_path() / dct["id"])["data"]


def _json_to_number(dct: dict) -> np.number:
    """
    Converts a JSON document to a numpy number. See `to_json` for the
    specification `dct` is expected to follow. Note that the key `__numpy__`
    should not be present.
    """
    DECODERS = {
        1: _json_to_number_v1,
        2: _json_to_number_v2,
    }
    return DECODERS[dct["__version__"]](dct)


def _json_to_number_v1(dct: dict) -> np.number:
    """
    Converts a JSON document to a numpy number following the v1 specification.
    """
    return np.frombuffer(
        dct["value"],
        dtype=np.lib.format.descr_to_dtype(dct["dtype"]),
    )[0]


def _json_to_number_v2(dct: dict) -> np.number:
    """
    Converts a JSON document to a numpy number following the v2 specification.
    """
    return np.frombuffer(dct["value"], dtype=dct["dtype"])[0]


def _json_to_random_state(dct: dict) -> np.number:
    """
    Converts a JSON document to a numpy random state. See `to_json` for the
    specification `dct` is expected to follow. Note that the key `__numpy__`
    should not be present.
    """
    DECODERS = {
        1: _json_to_random_state_v1,
    }
    return DECODERS[dct["__version__"]](dct)


def _json_to_random_state_v1(dct: dict) -> np.number:
    """
    Converts a JSON document to a numpy random state following the v1
    specification.
    """
    with open(get_artifact_path() / dct["data"], mode="rb") as fp:
        return pickle.load(fp)


def _dtype_to_json(d: np.dtype) -> dict:
    """Serializes a `numpy` array."""
    return {
        "__type__": "dtype",
        "__version__": 1,
        "dtype": np.lib.format.dtype_to_descr(d),
    }


def _ndarray_to_json(arr: np.ndarray) -> dict:
    """Serializes a `numpy` array."""
    return (
        _ndarray_to_json_v3(arr)
        if HAS_SAFETENSORS
        else _ndarray_to_json_v2(arr)
    )


def _ndarray_to_json_v2(arr: np.ndarray) -> dict:
    """
    Serializes a `numpy` array using the v2 format (which doesn't use
    `safetensors`)
    """
    if arr.nbytes <= get_max_nbytes():
        return {
            "__type__": "ndarray",
            "__version__": 2,
            "data": bytes(arr.data),
            "dtype": np.lib.format.dtype_to_descr(arr.dtype),
            "shape": arr.shape,
        }
    name = str(uuid4())
    np.save(get_artifact_path() / name, arr)
    return {
        "__type__": "ndarray",
        "__version__": 2,
        "id": name,
    }


def _ndarray_to_json_v3(arr: np.ndarray) -> dict:
    """
    Serializes a `numpy` array using the v3 format (which does use
    `safetensors`)
    """
    if arr.nbytes <= get_max_nbytes():
        return {
            "__type__": "ndarray",
            "__version__": 3,
            "data": st.save({"data": arr}),
        }
    name = str(uuid4())
    st.save_file({"data": arr}, get_artifact_path() / name)
    return {
        "__type__": "ndarray",
        "__version__": 3,
        "id": name,
    }


def _number_to_json(num: np.number) -> dict:
    """Serializes a `numpy` number."""

    return {
        "__type__": "number",
        "__version__": 2,
        "value": bytes(np.array(num).data),
        "dtype": num.dtype,
    }


def _random_state_to_json(obj: np.random.RandomState) -> dict:
    """Pickles a numpy random state"""
    name, protocol = str(uuid4()), pickle.HIGHEST_PROTOCOL
    with open(get_artifact_path() / name, mode="wb") as fp:
        pickle.dump(obj, fp, protocol=protocol)
    return {
        "__type__": "random_state",
        "__version__": 1,
        "data": name,
        "protocol": protocol,
    }


def from_json(dct: dict) -> Any:
    """
    Deserializes a dict into a numpy object. See `to_json` for the
    specification `dct` is expected to follow. In particular, note that `dct`
    must contain the key `__numpy__`.
    """
    raise_if_nodecode("numpy")
    DECODERS = {
        "ndarray": _json_to_ndarray,
        "number": _json_to_number,
        "dtype": _json_to_dtype,
        "random_state": _json_to_random_state,
    }
    try:
        type_name = dct["__numpy__"]["__type__"]
        raise_if_nodecode("numpy." + type_name)
        return DECODERS[type_name](dct["__numpy__"])
    except KeyError as exc:
        raise DeserializationError() from exc


def to_json(obj: Any) -> dict:
    """
    Serializes a `numpy` object into JSON by cases. See the README for the
    precise list of supported types.

    The return dict has the following structure

        {
            "__numpy__": {...},
        }

    where the `{...}` dict contains the actual data, and whose structure
    depends on the precise type of `obj`.

    - `numpy.ndarray`: An array is processed differently depending on its size
      and on the `TB_MAX_NBYTES` environment variable. If the array is
      small, i.e. `arr.nbytes <= TB_MAX_NBYTES`, then it is directly
      stored in the resulting JSON document as

            {
                "__numpy__": {
                    "__type__": "ndarray",
                    "__version__": 2,
                    "data": <ASCII encoded byte string>,
                    "dtype": <dtype_to_descr string>,
                    "shape": <int tuple>,
                }
            }

      or, if the `safetensors` package is available:

            {
                "__numpy__": {
                    "__type__": "ndarray",
                    "__version__": 3,
                    "data": <ASCII encoded byte string>,
                }
            }


      On the other hand, the array is too large (i.e. the number of bytes
      exceeds `TB_MAX_NBYTES` or the value set by
      `turbo_broccoli.environment.set_max_nbytes`), then the content of `arr`
      is stored in an `.npy` file. Said file is saved to the path specified by
      the `TB_ARTIFACT_PATH` environment variable with a
      random UUID4 as filename. The resulting JSON document looks like

            {
                "__numpy__": {
                    "__type__": "ndarray",
                    "__version__": <2 or 3>,
                    "id": <UUID4 str>,
                }
            }

      By default, `TB_MAX_NBYTES` is `8000` bytes, which should be enough
      to store an array of 1000 `float64`s, and `TB_ARTIFACT_PATH` is `./`.
      `TB_ARTIFACT_PATH` must point to an existing directory.

    - `numpy.number`:

            {
                "__numpy__": {
                    "__type__": "number",
                    "__version__": 2,
                    "value": <float>,
                    "dtype": {...},
                }
            }

        where the `dtype` document follows the specification below.

    - `numpy.dtype`:

            {
                "__numpy__": {
                    "__type__": "dtype",
                    "__version__": 1,
                    "dtype": <dtype_to_descr string>,
                }
            }

    - `numpy.random.RandomState`:

            {
                "__numpy__": {
                    "__type__": "random_state",
                    "__version__": 1,
                    "dtype": <uuid4>,
                    "protocol": <int>
                }
            }

      where the UUID4 points to a pickle file artefact, and the protocol is the
      pickle protocol.

    """
    ENCODERS: list[Tuple[type, Callable[[Any], dict]]] = [
        (np.ndarray, _ndarray_to_json),
        (np.number, _number_to_json),
        (np.dtype, _dtype_to_json),
        (np.random.RandomState, _random_state_to_json),
    ]
    for t, f in ENCODERS:
        if isinstance(obj, t):
            return {"__numpy__": f(obj)}
    raise TypeNotSupported()

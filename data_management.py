import os
import os.path
import pickle
from typing import Any, Callable

curdir = os.path.abspath(os.path.dirname(__file__))
logdir = os.path.join(curdir, "outputs")


def input_filepath(filename: str) -> str:
    return os.path.join(curdir, "training_data", filename)


def output_filepath(filename: str) -> str:
    return os.path.join(logdir, filename)


def save_data(filename: str, obj) -> None:
    """  """
    filepath = os.path.join(logdir, filename)
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)


def load_data(filename: str) -> Any:
    """  """
    filepath = os.path.join(logdir, filename)
    if not os.path.exists(filepath):
        return False

    with open(filepath, "rb") as f:
        return pickle.load(f)


def cached_call(id: str, call: Callable, *args, **kwargs) -> Any:
    """"  """
    filename = f"{id}.pickle"
    data = load_data(filename)
    if not data:
        data = call(*args, **kwargs)
        save_data(filename, data)
    return data

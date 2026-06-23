import numpy as np


### Currently being used by document service
def make_json_safe(obj):
    """
    Recursively converts non-JSON-serializable objects
    like numpy arrays into plain Python types.
    """

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_json_safe(i) for i in obj]

    if isinstance(obj, tuple):
        return [make_json_safe(i) for i in obj]

    return obj
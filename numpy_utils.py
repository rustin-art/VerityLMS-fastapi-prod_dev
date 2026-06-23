import numpy as np

## This Utils is used by service Api for Type constraint
def convert(obj):

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, dict):
        return {
            k: convert(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [
            convert(i)
            for i in obj
        ]

    return obj
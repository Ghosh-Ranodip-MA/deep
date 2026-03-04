import numpy as np
from typing import List

def normalize_scores(values: List[float]) -> List[float]:
    arr = np.array(values)
    if arr.size == 0 or arr.max() == arr.min():
        return [0.0] * len(arr)
    return ((arr - arr.min()) / (arr.max() - arr.min())).tolist()

def recency_score(year: int, current_year: int) -> float:
    if not year:
        return 0.0
    age = current_year - year
    if age <= 0:
        return 1.0
    return max(0.0, 1.0 - age / 20)
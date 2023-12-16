from typing import List

def add_numbers(x: int, y: int) -> int:
    return x + y

def map_add_numbers(num_list: List[int], x: int) -> List[int]:
    result = map(lambda y: y + x, num_list)
    return list(result)

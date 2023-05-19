from typing import Tuple, Dict, List

def getCoordinates(coords: List[Dict]) -> List[Tuple[int, int]]:
    return [(coord['x'], coord['y']) for coord in coords]

def getDictCoordinates(coords: List[Tuple[int, int]]) -> List[Dict]:
    return [{'x': x, 'y': y} for (x, y) in coords]
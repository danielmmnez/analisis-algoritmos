from functools import cmp_to_key
from typing import List

class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        # 1. Pasar todos los números a cadenas
        strs = [str(num) for num in nums]
        
        # 2. Definir el comparador basado en la concatenación
        def comparar(a: str, b: str) -> int:
            if a + b > b + a:
                return -1  # 'a' debe ir antes que 'b'
            elif a + b < b + a:
                return 1   # 'b' debe ir antes que 'a'
            else:
                return 0   # son equivalentes en orden
                
        # 3. Ordenar usando la clave personalizada
        strs.sort(key=cmp_to_key(comparar))
        
        # 4. Caso borde: si el mayor tras ordenar empieza con '0' (ej. [0, 0]), devolver "0"
        if strs[0] == "0":
            return "0"
            
        return "".join(strs)
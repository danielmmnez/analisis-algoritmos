from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        L = len(word)
        
        def backtrack(r: int, c: int, k: int) -> bool:
            # Caso base: ya encontramos todas las letras de la palabra
            if k == L:
                return True
                
            # Fuera de límites, celda ya usada o letra no coincide
            if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
                return False
                
            # 1. ELEGIR: guardamos el carácter actual y marcamos la celda como visitada
            temp = board[r][c]
            board[r][c] = "#"
            
            # 2. EXPLORAR: probamos los 4 vecinos ortogonales (abajo, arriba, derecha, izquierda)
            encontrado = (
                backtrack(r + 1, c, k + 1) or
                backtrack(r - 1, c, k + 1) or
                backtrack(r, c + 1, k + 1) or
                backtrack(r, c - 1, k + 1)
            )
            
            # 3. DESHACER (Backtrack): quitamos la marca restaurando la letra original
            board[r][c] = temp
            
            return encontrado

        # Lanzar la búsqueda desde cada celda de la grilla
        for fila in range(m):
            for col in range(n):
                if board[fila][col] == word[0] and backtrack(fila, col, 0):
                    return True
                    
        return False
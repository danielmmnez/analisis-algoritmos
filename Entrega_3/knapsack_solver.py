"""
Módulo del Solucionador de Programación Dinámica (Mochila 0/1)
Autor: Martín
Descripción:
    Implementa la formulación rigurosa de Programación Dinámica Bottom-Up:
    - Casos base
    - Relación de recurrencia
    - Llenado de matriz DP
    - Reconstrucción de items seleccionados
"""

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Suministro:
    id: int
    nombre: str
    peso_kg: int          # Peso entero (w_i)
    prioridad_salud: int  # Valor / Beneficio social (v_i)

class OptimizadorDronDP:
    """
    Solucionador de optimización de carga para drones médicos
    utilizando Programación Dinámica (0/1 Knapsack Problem).
    """

    def __init__(self, capacidad_maxima_kg: int):
        if capacidad_maxima_kg < 0:
            raise ValueError("La capacidad del dron no puede ser negativa.")
        self.capacidad_maxima = capacidad_maxima_kg

    def resolver(self, items: List[Suministro]) -> Tuple[int, List[List[int]], List[Suministro]]:
        """
        Ejecuta el algoritmo Bottom-Up de Programación Dinámica.

        Definición del Estado:
            dp[i][w] = Máxima prioridad médica alcanzable considerando
                       los primeros 'i' suministros con una capacidad de 'w' kg.

        Casos Base:
            dp[0][w] = 0 para todo w in [0, W] (sin paquetes, valor = 0)
            dp[i][0] = 0 para todo i in [0, N] (sin capacidad, valor = 0)

        Relación de Recurrencia:
            Si peso(i) > w:
                dp[i][w] = dp[i-1][w]
            Si peso(i) <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - peso(i)] + valor(i))
        """
        n = len(items)
        W = self.capacidad_maxima

        # 1. Inicialización de la tabla DP con casos base (todos en 0)
        dp = [[0] * (W + 1) for _ in range(n + 1)]

        # 2. Llenado iterativo Bottom-Up (O(N * W))
        for i in range(1, n + 1):
            item_actual = items[i - 1]
            w_i = item_actual.peso_kg
            v_i = item_actual.prioridad_salud

            for w in range(1, W + 1):
                if w_i > w:
                    # No cabe en la capacidad residual actual
                    dp[i][w] = dp[i - 1][w]
                else:
                    # Decisión binaria óptima (excluir vs incluir)
                    opcion_excluir = dp[i - 1][w]
                    opcion_incluir = dp[i - 1][w - w_i] + v_i
                    dp[i][w] = max(opcion_excluir, opcion_incluir)

        valor_optimo = dp[n][W]

        # 3. Algoritmo de Backtracking para reconstruir los ítems seleccionados
        items_seleccionados = self._reconstruir_solucion(dp, items, n, W)

        return valor_optimo, dp, items_seleccionados

    def _reconstruir_solucion(
        self, dp: List[List[int]], items: List[Suministro], n: int, W: int
    ) -> List[Suministro]:
        """
        Rastrea en retroceso la matriz DP para identificar exactamente
        qué suministros integran la solución óptima.
        """
        seleccionados = []
        cap_restante = W

        for i in range(n, 0, -1):
            if dp[i][cap_restante] != dp[i - 1][cap_restante]:
                item_incluido = items[i - 1]
                seleccionados.append(item_incluido)
                cap_restante -= item_incluido.peso_kg

        seleccionados.reverse()
        return seleccionados
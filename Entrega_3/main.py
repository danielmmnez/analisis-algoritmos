"""
Módulo Principal de Ejecución, Métricas y Visualización
Autor: Daniel
Descripción:
    - Interfaz de consola profesional y formateo de la matriz DP.
    - Análisis empírico de complejidad temporal y espacial.
    - Demostración comparativa de escenarios para la sustentación.
"""

import time
import sys
from typing import List
from knapsack_solver import Suministro, OptimizadorDronDP

def imprimir_separador(titulo: str = ""):
    print("\n" + "=" * 70)
    if titulo:
        print(f"  {titulo.upper()}")
        print("=" * 70)

def renderizar_matriz_dp(dp: List[List[int]], items: List[Suministro], W: int):
    """Muestra visualmente la tabla DP para la sustentación."""
    print("\n[TRAZA DE LA TABLA DE PROGRAMACIÓN DINÁMICA (Bottom-Up)]")
    encabezados = ["Item / Cap"] + [f"{w}kg" for w in range(W + 1)]
    fila_encabezado = " | ".join(f"{h:>7}" for h in encabezados)
    print("-" * len(fila_encabezado))
    print(fila_encabezado)
    print("-" * len(fila_encabezado))

    # Fila base i = 0
    fila_0 = [f"{dp[0][w]:>7}" for w in range(W + 1)]
    print(f"{'Base (0)':>10} | " + " | ".join(fila_0))

    # Filas para cada ítem
    for i, item in enumerate(items, 1):
        fila_vals = [f"{dp[i][w]:>7}" for w in range(W + 1)]
        etiqueta = f"i={i} ({item.peso_kg}k)"
        print(f"{etiqueta:>10} | " + " | ".join(fila_vals))
    print("-" * len(fila_encabezado))

def ejecutar_caso_clinico_real():
    imprimir_separador("Sistema de Despacho de Drones de Emergencia Médica")
    print("Hospital Central -> Zonas Rurales de Difícil Acceso")
    
    capacidad_dron = 15  # kg máximos de payload
    optimizador = OptimizadorDronDP(capacidad_maxima_kg=capacidad_dron)

    catalogo_emergencia = [
        Suministro(id=1, nombre="Antídotos / Suero Antiofídico", peso_kg=2, prioridad_salud=85),
        Suministro(id=2, nombre="Desfibrilador Externo (DEA)",   peso_kg=5, prioridad_salud=95),
        Suministro(id=3, nombre="Hemoderivados / Plasma O-",     peso_kg=4, prioridad_salud=90),
        Suministro(id=4, nombre="Kit Cirugía Menor y Suturas",   peso_kg=3, prioridad_salud=60),
        Suministro(id=5, nombre="Antibióticos Inyectables",      peso_kg=2, prioridad_salud=50),
        Suministro(id=6, nombre="Unidad Mini Concentrador O2",   peso_kg=7, prioridad_salud=80),
    ]

    print(f"\nCapacidad máxima de carga del Dron (W): {capacidad_dron} kg")
    print(f"Total de suministros médicos candidatos (N): {len(catalogo_emergencia)}")
    print("\nInventario disponible en base:")
    for s in catalogo_emergencia:
        print(f" - [{s.id}] {s.nombre:<32} | Peso: {s.peso_kg:2d} kg | Prioridad Médica: {s.prioridad_salud:3d} pts")

    # Medición de desempeño temporal
    inicio = time.perf_counter()
    valor_optimo, dp_tabla, seleccionados = optimizador.resolver(catalogo_emergencia)
    tiempo_ms = (time.perf_counter() - inicio) * 1000

    # Renderizar Matriz DP para explicar en el video
    renderizar_matriz_dp(dp_tabla, catalogo_emergencia, capacidad_dron)

    # Reporte de Resultados y Validación de Óptimo
    peso_total_usado = sum(s.peso_kg for s in seleccionados)
    
    imprimir_separador("Resultados de la Optimización (Plan de Vuelo)")
    print(f"\nPrioridad Médica Total Maximizada: {valor_optimo} puntos")
    print(f"Peso Total Embarcado:            {peso_total_usado} kg / {capacidad_dron} kg")
    print(f"Margen Residual de Peso:         {capacidad_dron - peso_total_usado} kg")
    print(f"Tiempo de Cómputo del Algoritmo: {tiempo_ms:.4f} ms")

    print("\nPaquetes cargados en la bahía del dron:")
    for idx, item in enumerate(seleccionados, 1):
        print(f" {idx}. {item.nombre:<32} (Peso: {item.peso_kg} kg, Valor: {item.prioridad_salud})")

    imprimir_separador("Análisis Teórico de Complejidad")
    n = len(catalogo_emergencia)
    W = capacidad_dron
    estados_computados = (n + 1) * (W + 1)
    
    print(f" - Complejidad Temporal Teórica:  O(N * W) -> {n} * {W} = {n * W} operaciones fundamentales")
    print(f" - Complejidad Espacial Teórica:  O(N * W) -> {estados_computados} celdas en memoria")
    print(f" - Comparación vs Fuerza Bruta:   O(2^{n}) = {2**n} combinaciones evaluadas")
    print(f" - Factor de Eficiencia:          {(2**n) / (n*W):.2f}x menos combinaciones exploradas")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    ejecutar_caso_clinico_real()
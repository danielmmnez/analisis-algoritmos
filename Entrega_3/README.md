# Despacho Óptimo de Drones Médicos: Programación Dinámica (Mochila 0/1)

Examen 3 — Análisis de Algoritmos

Desarrollo de un sistema de optimización utilizando Programación Dinámica para resolver un problema de logística médica en emergencias.

## Descripción del problema

En situaciones de desastre natural o emergencias en zonas rurales de difícil acceso, el transporte terrestre queda bloqueado o toma tiempos inviables. Los drones de carga médica permiten llevar insumos críticos de manera inmediata, pero cuentan con una restricción física severa: **su capacidad máxima de carga (*payload*) es limitada y estricta**.

Cada suministro médico tiene un peso entero en kilogramos y un valor de prioridad médica (beneficio social y clínico asignado por triaje). Además, los suministros son **indivisibles** (no es posible fraccionar un desfibrilador, un antídoto o un kit quirúrgico). 

Se plantea el problema de seleccionar el subconjunto óptimo de suministros que:
- No supere la capacidad máxima de carga útil del dron ($W = 15\text{ kg}$).
- Maximice el beneficio de prioridad médica total transportado.
- Supere las limitaciones de los algoritmos voraces (*Greedy*), los cuales no garantizan el óptimo global ante insumos indivisibles.

## Solución

El problema se modeló formalmente como una instancia del **Problema de la Mochila 0/1 (*0/1 Knapsack Problem*)** y se resolvió mediante **Programación Dinámica Bottom-Up**, garantizando la subestructura óptima y evitando el recálculo exponencial de subproblemas superpuestos.

### Modelo del problema

| Elemento | Representa | Detalle |
|---|---|---|
| Objeto $i$ | Suministro médico | Elemento indivisible con peso y prioridad asociada |
| Peso $w_i$ | Peso del insumo en kg | Carga física que consume capacidad del dron |
| Valor $v_i$ | Prioridad médica (1-100) | Beneficio clínico y vital del suministro |
| Capacidad $W$ | Carga útil máxima (*payload*) | Restricción dura: $15\text{ kg}$ |
| Variable $x_i \in \{0, 1\}$ | Decisión binaria | $0 = \text{Excluir del dron}$, $1 = \text{Embarcar en el dron}$ |

### Estructura modular del proyecto

El desarrollo se dividió en dos módulos para separar la formulación algorítmica de la capa de visualización y análisis de complejidad:

1. knapsack_solver.py:
   - Definición de entidades de datos (`Suministro`).
   - Casos base y relación de recurrencia.
   - Construcción de la matriz DP en memoria (*Bottom-Up*).
   - Algoritmo de *Backtracking* para reconstruir la lista de suministros seleccionados.
2. main.py:
   - Configuración del escenario de emergencia hospitalario.
   - Renderizado tabular formateado de la matriz DP en consola.
   - Medición de rendimiento empírico en microsegundos.
   - Cálculo analítico de complejidades temporal $O(N \cdot W)$ y espacial $O(N \cdot W)$.


### Enlace video

[Enlace video sustentación](https://correoitmedu-my.sharepoint.com/:v:/g/personal/martinzapata319040_correo_itm_edu_co/IQDyD-RtAaQFRqzMMmOxsZZ_AZaMHo_J-mPhyMEsO7ZpJ3A?e=rG1BuX&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

### Instrucciones de ejecución

El código utiliza únicamente la biblioteca estándar de Python (no requiere librerías externas adicionales):

```bash
python main.py
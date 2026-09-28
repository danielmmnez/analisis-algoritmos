# Ruta óptima en Medellín: Dijkstra vs A*
 
Examen 2 — Análisis de Algoritmos
 
Opción 2: Presentación explicando un algoritmo de grafos y su aplicación a un problema real.
 
## Descripción del problema
 
Aplicaciones de movilidad y GPS resuelven todos los días una pregunta aparentemente simple: dado un origen y un destino en una ciudad, ¿cuál es el mejor camino? El detalle es que "mejor" no significa "más corto en metros", sino **más rápido en minutos**. Una vía más larga pero con mayor velocidad permitida puede ser más eficiente que un atajo lento, así que el costo real de recorrer una calle es el tiempo, no la distancia.
 
Se plantea entonces el problema de encontrar la ruta de menor tiempo entre un origen y un destino de la red vial real de Medellín, Colombia. Se necesita un algoritmo que:
 
- Trabaje sobre datos reales de calles (miles de intersecciones y vías, cada una con su longitud y su velocidad máxima).
- Garantice que la ruta encontrada es la óptima, es decir, la de menor tiempo total.
- Permita comparar qué tanto esfuerzo de búsqueda (nodos explorados) requiere cada estrategia para llegar al mismo destino.
 
## Solución
 
Se modeló la red vial como un **grafo dirigido y ponderado** y se implementaron dos algoritmos de camino mínimo para compararlos:
 
- **Dijkstra**, algoritmo principal: minimiza el tiempo de viaje y garantiza la ruta óptima porque todos los pesos (tiempos) son no negativos.
- **A\***, algoritmo de comparación: explora con dirección hacia el destino mediante una heurística (distancia en línea recta), lo que reduce el número de nodos explorados frente a Dijkstra.
 
### Modelo del grafo
 
| Elemento | Representa | Detalle |
|---|---|---|
| Vértice | Intersección de la ciudad | Nodos del grafo de OpenStreetMap |
| Arista | Calle (dirigida) | Respeta el sentido de circulación de cada vía |
| Peso | Tiempo estimado de recorrido | `longitud / velocidad máxima` de la vía |
 
Los datos se extraen con `osmnx` desde OpenStreetMap (`network_type="drive"`). La velocidad máxima de cada vía se limpia antes de calcular el peso: si el dato viene como lista se toma el valor mínimo, si es texto se convierte a entero, y si la vía no tiene dato se asume 40 km/h.
 
### Implementación
 
El código está en el notebook [`grafos_examen2.ipynb`](./grafos.ipynb) y usa tres piezas principales:
 
1. **osmnx**: descarga el grafo de Medellín y permite dibujarlo.
2. **networkx** (estructura de grafo que devuelve osmnx): manejo de vértices, aristas y atributos.
3. **heapq**: cola de prioridad (min-heap) que selecciona el siguiente vértice a explorar en O(log n).
 
El origen y el destino son **fijos** (definidos por dos direcciones reales, geocodificadas y convertidas a su nodo más cercano), de modo que el resultado es reproducible. Además, el notebook incluye una **animación** que redibuja el mapa mientras cada algoritmo se expande, y un experimento de 100 rutas aleatorias con mapas de calor de las calles más usadas por cada algoritmo.
 
Para ejecutarlo:
 
```bash
pip install osmnx matplotlib
jupyter notebook grafos.ipynb
```
 
## Explicación del algoritmo
 
### Dijkstra (algoritmo principal)
 
Dijkstra expande la búsqueda como una onda en un estanque: parte del origen y avanza siempre hacia el nodo aún no visitado con **menor tiempo acumulado** `g(n)`, sin saber dónde está el destino. En cada paso:
 
1. **Extraer** de la cola de prioridad el nodo no visitado con menor tiempo acumulado.
2. **Relajar** sus aristas: calcular el tiempo hacia cada vecino pasando por ese nodo.
3. **Actualizar** la cola de prioridad y el nodo "anterior" del vecino si se encontró un camino más rápido.
 
El algoritmo termina cuando el destino sale de la cola, y la ruta se reconstruye siguiendo los nodos "anteriores" desde el destino hasta el origen.
 
**Garantía de optimalidad**: cuando un nodo sale de la cola, ya no puede existir un camino más rápido hacia él, siempre que ningún peso sea negativo. Aquí los pesos son tiempos, por lo tanto nunca lo son.
 
**Complejidad**: con un min-heap es O((n + m) log n), donde `n` es el número de intersecciones y `m` el de calles.
 
### A* (comparación)
 
A* parte de la misma idea, pero ordena la cola por:
 
```
f(n) = g(n) + h(n)
```
 
- `g(n)`: costo acumulado desde el origen (igual que en Dijkstra).
- `h(n)`: heurística, una estimación de lo que falta hasta el destino; en este proyecto, la distancia en línea recta.
 
Al sumar `h(n)`, los nodos que apuntan hacia el destino quedan con menor `f` que los que se alejan, así que la búsqueda se estrecha en un corredor hacia el destino en vez de expandirse en todas direcciones. Para conservar la garantía de ruta óptima, la heurística debe ser **admisible**: nunca puede sobreestimar el costo real. Si `h(n) = 0` para todos los nodos, A* se comporta exactamente como Dijkstra.
 
| Algoritmo | Prioriza por | Conoce el destino | Exploración | Garantía de óptimo | Uso ideal |
|---|---|---|---|---|---|
| Dijkstra | `g(n)` | No | En todas direcciones | Sí (pesos ≥ 0) | Múltiples destinos o redes sin coordenadas |
| A* | `g(n) + h(n)` | Sí, vía heurística | Dirigida al destino | Sí (heurística admisible) | Ruteo punto a punto en mapas geográficos |
 
## Resultados
 
Ruta entre **[origen]** y **[destino]**:
 
| Métrica | Dijkstra | A* |
|---|---|---|
| Distancia total | 9.58 km | [X] km |
| Velocidad promedio | 55.49 km/h | [X] km/h |
| Tiempo estimado | 10.35 min | [X] min |
| Nodos explorados | 5277 | [X] |
 
Observaciones:
 
- Dijkstra explora de forma pareja en todas direcciones; A* concentra la búsqueda en un corredor hacia el destino y visita menos nodos.
- Los mapas de calor de 100 rutas aleatorias muestran qué calles usa con más frecuencia cada algoritmo.
 
### Limitaciones
 
- La implementación de A* acumula como costo la distancia geométrica entre nodos (no el tiempo `longitud / velocidad`), así que A* busca el camino más corto guiado por línea recta, mientras que Dijkstra minimiza el tiempo. Ambos son búsquedas de camino mínimo válidas, pero no optimizan exactamente la misma métrica, y por eso la comparación de nodos explorados es una comparación de estrategia de búsqueda más que de resultado idéntico.
- El peso usa la velocidad **máxima** permitida, no el tráfico real, por lo que el tiempo estimado es una cota optimista.

## Video sustentación

[Enlace Video](https://correoitmedu-my.sharepoint.com/:v:/g/personal/danielmartinez315751_correo_itm_edu_co/IQC_k_AjBYMzTqAB6Vffu0Y6AayouMONxvygPFD9fcJgTww?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=wbY05K)
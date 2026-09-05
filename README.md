# analisis-algoritmos

Repositorio compartido clase de analisis de algoritmos

# integrantes

Daniel Martinez Martinez
Martin Zapata Franco



\*\*Estabilidad\*\*: la clave está en la comparación durante la fusión:

&#x20;

```python

if izquierda\[i].fecha\_limite <= derecha\[j].fecha\_limite:

```

&#x20;

El operador es `<=` (menor o igual), no `<` estricto. Cuando hay empate, esta condición se cumple y se toma primero el elemento de la mitad \*\*izquierda\*\*, que es la que contiene los elementos que llegaron antes en la lista original. Ese es el detalle que hace estable al algoritmo.

&#x20;

\### Insertion Sort (comparación)

&#x20;

Recorre la lista de izquierda a derecha y, para cada elemento, lo desplaza hacia atrás hasta encontrar su posición correcta dentro del segmento ya ordenado.

&#x20;

\- \*\*Adaptativo\*\*: si la entrada llega casi ordenada, el número de desplazamientos es mínimo y el costo cae a θ(n).

\- \*\*Riesgo\*\*: si la entrada llega en desorden total (el caso real de este problema), el costo se dispara a θ(n²).

\- También es estable (usa `>` estricto al comparar hacia atrás), pero no se eligió como solución principal porque su rendimiento no es robusto frente al desorden de la entrada.

| Algoritmo | Peor caso | Memoria extra | Adaptativo | Estable | Uso ideal |

|---|---|---|---|---|---|

| Merge Sort | θ(n log n) | θ(n) | No | Sí | Lotes masivos y desordenados desde cero |

| Insertion Sort | θ(n²) | O(1) | Sí (mejor: θ(n)) | Sí | Insertar un cliente rezagado en una lista ya procesada |


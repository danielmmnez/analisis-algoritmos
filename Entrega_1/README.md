# Priorización de declaraciones DIAN mediante ordenamiento
 
Examen 1 — Análisis de Algoritmos
Opción 2: Presentación explicando un algoritmo de ordenamiento y su aplicación a un problema.
 
## Descripción del problema
 
Como contador que gestiona las declaraciones de renta de varios clientes ante la DIAN, es necesario priorizar en qué orden atenderlos según su fecha límite de declaración. Esa fecha la asigna la DIAN de forma determinista según los dos últimos dígitos de la cédula o NIT de cada persona — un criterio que no tiene ninguna relación con el momento en que el cliente entrega sus documentos.
 
Como resultado, la lista de clientes se acumula en un orden completamente desligado de sus fechas límite: dos clientes pueden llegar consecutivos y tener plazos muy distantes entre sí, o llegar muy separados y compartir exactamente la misma fecha (algo frecuente, porque cada pareja de dígitos del NIT comparte plazo). Se necesita entonces un algoritmo que:
 
- Ordene la lista de clientes por `fecha_limite`.
- Tenga un rendimiento robusto sin importar qué tan desordenada llegue la entrada, ya que no se puede asumir ninguna estructura previa en los datos.
- Resuelva de forma predecible los casos en que dos clientes comparten la misma fecha límite, dando prioridad a quien lleva más tiempo esperando ser atendido.
## Solución
 
Se implementó **Merge Sort**, que ordena la lista por fecha límite de declaración sin que el desorden de la entrada afecte su rendimiento — su complejidad es θ(n log n) en el mejor, peor y caso promedio, a diferencia de algoritmos como Insertion Sort cuyo rendimiento sí depende de qué tan ordenada venga la entrada.
 
Además, se aprovechó que Merge Sort es un algoritmo **estable**: cuando dos clientes comparten la misma fecha límite, se conserva automáticamente el orden en que llegaron originalmente a la lista, sin necesidad de programar una regla de desempate adicional.
 
Como comparación, también se incluye una implementación de **Insertion Sort**, útil para mostrar el trade-off: es más eficiente que Merge Sort cuando la entrada ya llega casi ordenada, pero su rendimiento se degrada a θ(n²) en el caso desordenado que corresponde a este problema.
 
## Explicación del algoritmo
 
### Merge Sort (algoritmo principal)
 
Merge Sort sigue la estrategia de **divide y vencerás**, en dos pasos:
 
1. **Dividir**: la lista se parte recursivamente por la mitad, ignorando por completo el desorden inicial, hasta llegar a sublistas de un solo elemento (trivialmente ordenadas).
2. **Fusionar**: las sublistas ya ordenadas se combinan en una sola, comparando en cada paso únicamente los elementos al frente de cada sublista — el menor de los dos pasa primero al resultado.
**Complejidad**: cada división genera un nivel nuevo en el árbol de recursión, y como siempre se parte por la mitad, hay `log₂ n` niveles. En cada nivel, fusionar recorre los `n` elementos completos, es decir, cuesta O(n). Multiplicando niveles por costo por nivel se obtiene θ(n log n) — igual en el mejor, peor y caso promedio, porque el paso de dividir no depende del orden de la entrada.

**Estabilidad**: la clave está en la comparación durante la fusión:
 
```python
if izquierda[i].fecha_limite <= derecha[j].fecha_limite:
```
 
El operador es `<=` (menor o igual), no `<` estricto. Cuando hay empate, esta condición se cumple y se toma primero el elemento de la mitad **izquierda**, que es la que contiene los elementos que llegaron antes en la lista original. Ese es el detalle que hace estable al algoritmo.
 
### Insertion Sort (comparación)
 
Recorre la lista de izquierda a derecha y, para cada elemento, lo desplaza hacia atrás hasta encontrar su posición correcta dentro del segmento ya ordenado.
 
- **Adaptativo**: si la entrada llega casi ordenada, el número de desplazamientos es mínimo y el costo cae a θ(n).
- **Riesgo**: si la entrada llega en desorden total (el caso real de este problema), el costo se dispara a θ(n²).
- También es estable (usa `>` estricto al comparar hacia atrás), pero no se eligió como solución principal porque su rendimiento no es robusto frente al desorden de la entrada.

| Algoritmo | Peor caso | Memoria extra | Adaptativo | Estable | Uso ideal |
|---|---|---|---|---|---|
| Merge Sort | θ(n log n) | θ(n) | No | Sí | Lotes masivos y desordenados desde cero |
| Insertion Sort | θ(n²) | O(1) | Sí (mejor: θ(n)) | Sí | Insertar un cliente rezagado en una lista ya procesada |

## Video de sustentación
 
[Sustentación](https://correoitmedu-my.sharepoint.com/:v:/g/personal/martinzapata319040_correo_itm_edu_co/IQAcZXWzu3TtSYLQ-sVFl_WcAR3_-SVVY9ioVxw4wi5jbmY?e=pTmXYR&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
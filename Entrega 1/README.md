# Priorización de declaraciones DIAN mediante ordenamiento
 
Examen 1 — Análisis de Algoritmos
Opción 2: Presentación explicando un algoritmo de ordenamiento y su aplicación a un problema real.
 
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
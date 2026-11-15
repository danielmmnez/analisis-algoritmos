"""
Ordenamiento de clientes para declaración de renta por fecha límite de declaración.
 
Problema: los clientes se van acumulando en una lista SIN ningún orden
respecto a su fecha límite (la DIAN la asigna según los dos últimos
dígitos del NIT/cédula, algo que no tiene relación con cuándo el cliente
entrega sus documentos). Es decir, la entrada llega desordenada — el
"Caso 2" que discutimos, donde Merge Sort es la opción robusta porque su
costo θ(n log n) no depende del orden de entrada.
 
El campo `orden_llegada` guarda explícitamente la posición en la que el
cliente entró a la lista original. No se usa como criterio principal de
ordenamiento (ese es fecha_limite), pero es lo que la ESTABILIDAD del
algoritmo aprovecha automáticamente: si dos clientes comparten la misma
fecha límite (algo esperable, porque cada pareja de dígitos del
NIT/cédula comparte fecha), el que tenga menor orden_llegada queda
primero — sin que el algoritmo lo compare explícitamente.
"""
 
from dataclasses import dataclass
from datetime import date
 
 
@dataclass
class Cliente:
    nombre: str
    fecha_limite: date
    orden_llegada: int  # posición original en la lista; usado solo como desempate implícito vía estabilidad
 
    def __repr__(self) -> str:
        return f"{self.nombre} ({self.fecha_limite.strftime('%d %b')}, llegó #{self.orden_llegada})"
 
 
# ---------------------------------------------------------------------------
# Insertion Sort
# ---------------------------------------------------------------------------
# Idea: recorrer la lista de izquierda a derecha. En cada paso, tomar el
# elemento actual y desplazarlo hacia atrás mientras haya elementos mayores
# que él, insertándolo justo en su posición correcta dentro del segmento
# ya ordenado.
#
# Es adaptativo: si la lista ya llega casi ordenada (caso común cuando los
# clientes van entregando documentos progresivamente, cerca de su propia
# fecha límite), el número de desplazamientos hacia atrás es pequeño y el
# algoritmo se acerca a un costo O(n).
#
# Complejidad: mejor caso θ(n) | promedio θ(n²) | peor caso θ(n²)
 
def insertion_sort(clientes: list[Cliente]) -> list[Cliente]:
    lista = clientes.copy()  # no mutar la lista original
    comparaciones = 0
 
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
 
        # Desplazar hacia la derecha mientras el elemento anterior sea
        # ESTRICTAMENTE mayor. El "<" (no "<=") es lo que garantiza la
        # estabilidad: si hay empate en fecha_limite, no se intercambia.
        while j >= 0 and lista[j].fecha_limite > actual.fecha_limite:
            comparaciones += 1
            lista[j + 1] = lista[j]
            j -= 1
        if j >= 0:
            comparaciones += 1
 
        lista[j + 1] = actual
 
    insertion_sort.comparaciones = comparaciones
    return lista

# ---------------------------------------------------------------------------
# Merge Sort
# ---------------------------------------------------------------------------
# Idea: dividir la lista a la mitad recursivamente hasta llegar a listas
# de un solo elemento (trivialmente ordenadas), y luego fusionar ("merge")
# las mitades ya ordenadas en una sola lista ordenada.
#
# No es adaptativo: su costo no depende del orden de entrada, siempre
# divide y fusiona de la misma manera. Por eso es la opción robusta cuando
# el reporte se genera desde cero con datos de origen desordenado.
#
# Complejidad: mejor caso θ(n log n) | promedio θ(n log n) | peor caso θ(n log n)
# Costo extra: θ(n) de memoria auxiliar para la fusión.
 
def merge_sort(clientes: list[Cliente]) -> list[Cliente]:
    if len(clientes) <= 1:
        return clientes
 
    mitad = len(clientes) // 2
    izquierda = merge_sort(clientes[:mitad])
    derecha = merge_sort(clientes[mitad:])
 
    return _fusionar(izquierda, derecha)
 
 
def _fusionar(izquierda: list[Cliente], derecha: list[Cliente]) -> list[Cliente]:
    resultado: list[Cliente] = []
    i = j = 0
 
    while i < len(izquierda) and j < len(derecha):
        # "<=" en vez de "<": si hay empate, tomamos primero el elemento
        # de la mitad IZQUIERDA, que es la que apareció antes en la lista
        # original. Esa elección es lo que hace estable al algoritmo.
        if izquierda[i].fecha_limite <= derecha[j].fecha_limite:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
 
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado
 
 
# ---------------------------------------------------------------------------
# Demostración
# ---------------------------------------------------------------------------
 
if __name__ == "__main__":
    # orden_llegada se asigna según la posición en la lista de entrada,
    # simulando el orden real en que cada cliente entregó sus documentos.
    nombres_y_fechas = [
        ("Cliente A", date(2026, 9, 15)),
        ("Cliente B", date(2026, 9, 10)),
        ("Cliente C", date(2026, 9, 10)),  # empatado con B en fecha_limite
        ("Cliente D", date(2026, 9, 20)),
    ]
    clientes = [
        Cliente(nombre, fecha, orden_llegada=i)
        for i, (nombre, fecha) in enumerate(nombres_y_fechas)
    ]
 
    print("Lista original (orden de llegada):")
    print(clientes)

    ordenado_merge = merge_sort(clientes)
    print("\nOrdenada con Merge Sort (por fecha_limite):")
    print(ordenado_merge)
 
    ordenado_insertion = insertion_sort(clientes)
    print("\nOrdenada con Insertion Sort (por fecha_limite):")
    print(ordenado_insertion)
    print(f"Comparaciones realizadas: {insertion_sort.comparaciones}")

    # Verificación explícita del desempate: entre los clientes con la
    # misma fecha_limite, orden_llegada debe quedar en orden ascendente.
    empatados = [c for c in ordenado_merge if c.fecha_limite == date(2026, 9, 10)]
    ordenes = [c.orden_llegada for c in empatados]
    assert ordenes == sorted(ordenes), "El desempate por orden de llegada se perdió"
    print(f"\nDesempate verificado: entre los empatados, quedaron en orden de llegada {ordenes}")
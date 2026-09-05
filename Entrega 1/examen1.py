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
# Demostración aislada
# ---------------------------------------------------------------------------
 
if __name__ == "__main__":
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
 
    ordenado_insertion = insertion_sort(clientes)
    print("\nOrdenada con Insertion Sort (por fecha_limite):")
    print(ordenado_insertion)
    print(f"Comparaciones realizadas: {insertion_sort.comparaciones}")
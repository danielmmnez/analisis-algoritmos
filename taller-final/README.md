## 215. Kth Largest Element in an Array

- **Problema:** [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- **Autor:** Tu Nombre (`danielmmnez`)
- **Familia:** Heap 
- **Idea:** Mantenemos un min-heap acotado a un tamaño máximo `k`. Recorremos `nums`: mientras el heap tenga menos de `k` elementos, insertamos; si ya tiene `k` y el elemento actual supera a la raíz (el mínimo entre los `k` mejores candidatos), reemplazamos la raíz. Al finalizar, la raíz contiene el k-ésimo mayor.
- **Complejidad:** Tiempo `O(n log k)` y Espacio extra `O(k)`, donde `n = nums.length` y `k` es la capacidad máxima del heap.

![Accepted — Kth Largest](evidencias/kth-largest-accepted.png)
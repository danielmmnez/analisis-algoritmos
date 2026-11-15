import heapq
from typing import List

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Min-heap que guardará a lo sumo k elementos
        min_heap = []
        
        for num in nums:
            if len(min_heap) < k:
                heapq.heappush(min_heap, num)
            elif num > min_heap[0]:
                # Si el número actual es mayor que el menor de los k grandes,
                # sacamos la raíz e insertamos el nuevo (heappushpop lo hace en un paso)
                heapq.heappushpop(min_heap, num)
                
        # La raíz del min-heap es el k-ésimo elemento más grande
        return min_heap[0]
from typing import List

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # Si el gas total no alcanza para cubrir el costo total, es imposible
        if sum(gas) < sum(cost):
            return -1
            
        tanque = 0
        inicio_candidato = 0
        
        for i in range(len(gas)):
            tanque += gas[i] - cost[i]
            
            # Si el tanque queda negativo, ninguna estación del tramo [inicio_candidato..i] sirve
            if tanque < 0:
                inicio_candidato = i + 1
                tanque = 0
                
        return inicio_candidato
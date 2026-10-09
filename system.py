from objects import Objects
from ast import List
def GravitationSystem(objects: List[Objects]):
    for i in range(len(objects)):
        for j in range(len(objects)):
            if i == j:
                continue
            objects[i].GravitationForce(objects[j])
    
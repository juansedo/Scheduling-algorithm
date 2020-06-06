import time
import csv
import inits
from pathlib import Path
import graphs

start_time = time.time()

# Inicializaciones de datos
distancias = inits.distanciasInit()
aulas = inits.aulasInit()
estudiantes = inits.estudiantesInit()
clases = inits.clasesInit()
inits.matriculasInit(estudiantes, clases)

# Limpieza de información
clases = [x for x in clases if x.numberOfStudents > 0 and x.room != 0]
arrived_clases = inits.arrivedClasesInit(estudiantes)
arrived_clases = [x for x in arrived_clases if x.numberOfStudents > 0 and x.room != 0]

for clase in arrived_clases:
    print(clase.room)

print ("Total: ", len(arrived_clases))
print("old distance= " + str(graphs.calcDistances(arrived_clases, distancias)))
inits.initAvailabilities(clases, aulas)
arrived_clases.sort(key=lambda x: (int(x.impairment), x.numberOfStudents))

for clase in arrived_clases:
    graphs.AssignRooms(clase, distancias, aulas)

for clase in arrived_clases:
    print(clase.room)

print ("Total: ", len(arrived_clases))
print("new distance= " + str(graphs.calcDistances(arrived_clases, distancias)))
print("--- %s seconds ---" % (time.time() - start_time))

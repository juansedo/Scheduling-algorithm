import time
import inits
import graphs
import copy

times = {}
start_time = time.time()

# Inicializaciones de datos
distancias = inits.distanciasInit()
aulas = inits.aulasInit()
estudiantes = inits.estudiantesInit()
clases = inits.clasesInit()
inits.matriculasInit(estudiantes, clases, aulas)
times['init'] = time.time()

# Limpieza de información y arrived clases
clases = [x for x in clases if x.numberOfStudents > 0 and x.room != 0]
arrived_clases = inits.arrivedClasesInit(estudiantes)
arrived_clases = [x for x in arrived_clases if x.numberOfStudents > 0 and x.room != 0]
times['clean'] = time.time()

# Guardando información de antes
old_arrived_clases = {cl.__repr__(): cl for cl in copy.deepcopy(arrived_clases)}
times['s_old'] = time.time()

# Algoritmo
inits.initAvailabilities(clases, aulas)
arrived_clases.sort(key=lambda x: (int(x.impairment), x.numberOfStudents))
for clase in arrived_clases:
    graphs.AssignRooms(clase, distancias, aulas)
times['exec'] = time.time()                    # Stop del cronómetro

# Guardando información de después
new_arrived_clases = {cl.__repr__(): cl for cl in copy.deepcopy(arrived_clases)}
times['s_new'] = time.time()

# Imprimiendo información
print("BEFORE...\t\t\t\t\tNOW...")
graphs.print_comparison(distancias, old_arrived_clases, new_arrived_clases)
print("TOTAL DISTANCE :", str(graphs.calcDistances(old_arrived_clases.values(), distancias)), end='\t\t\t\t')
print("TOTAL DISTANCE :", str(graphs.calcDistances(new_arrived_clases.values(), distancias)))

times['s_new'] -= times['exec']
times['exec'] -= times['s_old']
times['s_old'] -= times['clean']
times['clean'] -= times['init']
times['init'] -= start_time
print("\nTimes:")
for t, v in times.items():
    print(t,":\t",v,"s")
print("TOTAL TIME:", sum(times.values()),"s")

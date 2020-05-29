import time
import csv
import inits
from pathlib import Path
import graphs

start_time = time.time()

aulas = inits.aulasInit()
estudiantes = inits.estudiantesInit()
clases = inits.clasesInit()
distancias = inits.distanciasInit()

map_of_clases = inits.mappingClases(clases)

path = Path(__file__).parent / "mat20192.csv"
with open(path, encoding="utf8") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  reg = 0
  for row in csv_reader:
    if estudiantes.get(row[0]) is not None:
      id_clase = row[1]+"."+row[2]
      if map_of_clases.get(id_clase) is not None:
        estudiantes[row[0]].addClass(map_of_clases[id_clase])
        reg +=1
    line_count += 1
  print(f'mat20192 file: Processed {line_count} lines ({reg} registered).')

clases_simples = inits.clasesSimplesInit(estudiantes)

def findClassrooms(aulas, distancias, clases_simples, clase):
  clase = clases_simples.get(clase)
  if clase is None or clase.visited or len(clase.arrivals.keys()) == 0:
    return
  isThereZero = 0
  clase.visited = True
  dist_totales = []
  for b in distancias.keys():
    if b == 28: continue
    total = 0
    for key, value in clase.arrivals.items():
      if value['block'] == 0 and clases_simples.get(key) is not None:
        findClassrooms(aulas, distancias, clases_simples, key)
      elif value['block'] == 0:
        isThereZero += 1
        continue
      elif distancias[b].get(value['block']) is None:
        continue
      total += value['amount'] * distancias[b][value['block']]
    dist_totales.append([b, total])
  clase.distances = sorted(dist_totales, key= lambda elem: elem[1])
  
  for dist in clase.distances:
    if clase.room != 0 and not isThereZero: return
    if aulas.get(dist[0]) is None: continue
    possible_rooms = [x for x in aulas[dist[0]].keys() if aulas[dist[0]][x].available]
    if len(possible_rooms) > 0:
      if clase.room == 0:
        clase.room = possible_rooms.pop(0)
        aulas[dist[0]][clase.room].available = False
        
      if isThereZero > 0:
        for key in clase.arrivals.keys():
          if len(possible_rooms) == 0: continue          
          if clase.arrivals[key]['block'] == 0:
            if clases_simples.get(key) is not None:
              clases_simples[key].room = possible_rooms.pop(0)
              clase.arrivals[key]['block'] = clases_simples[key].room // 1000
            
  
for i in clases_simples.keys():
  findClassrooms(aulas, distancias, clases_simples, i)
  print(i, ",", clases_simples[i], ".\n", clases_simples[i].distances)

print("--- %s seconds ---" % (time.time() - start_time))
#valids = graphs.getValidClasses(estudiantes)
#posibles_distancias = graphs.analizeDistances(valids, distancias)
#for i in posibles_distancias.keys():
#    print(i)
#    print(posibles_distancias[i])
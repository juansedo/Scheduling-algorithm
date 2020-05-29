import csv
import inits
from pathlib import Path
import graphs

def clasesById(clases, class_id, group):
  set_class = set([])
  for cl in clases:
    if cl.code == class_id and str(cl.group) == group:
      set_class.add(cl)
  return set_class

aulas = inits.aulasInit()
estudiantes = inits.estudiantesInit()
clases = inits.clasesInit()
distancias = inits.distanciasInit()

path = Path(__file__).parent / "mat20192.csv"
with open(path, encoding="utf8") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  reg = 0
  for row in csv_reader:
    if estudiantes.get(row[0]) is not None:
      estudiantes[row[0]].addClass(clasesById(clases, row[1], row[2]))
      reg +=1
    line_count += 1
  print(f'mat20192 file: Processed {line_count} lines ({reg} registered).')

clases_simples = inits.clasesSimplesInit(estudiantes)

def findClassrooms(aulas, distancias, clases_simples, clase):
  clase = clases_simples.get(clase)
  if clase.visited or len(clase.arrivals) == 0:
    return
  clase.visited = True
  dist_totales = []
  isThereZero = False
  for b in distancias.keys():
    if b == 28: continue
    total = 0
    for key, value in clase.arrivals.items():
      if value['block'] == 0 and clases_simples.get(key) is not None:
        findClassrooms(aulas, distancias, clases_simples, key)
      elif value['block'] == 0:
        isThereZero = True
        continue
      elif distancias[b].get(value['block']) is None:
        continue
      total += value['amount'] * distancias[b][value['block']]
    dist_totales.append([total, b])
  clase.distances = sorted(dist_totales, key= lambda elem: elem[0])
  
  if isThereZero:
    for key, value in clase.arrivals.items():
      if value['block'] == 0:
        value['block'] = clase.room//1000
    return findClassrooms(aulas, distancias, clases_simples, clase)

  for dist in clase.distances:
    if aulas.get(dist[1]) is None: continue
    possible_rooms = [x for x in aulas[dist[1]].keys() if aulas[dist][x].available]
    if len(possible_rooms) > 0:
      clase.room = possible_rooms[0]
      aulas[dist][x].available = False
  

for i in clases_simples.keys():
  findClassrooms(aulas, distancias, clases_simples, i)
  print(i, ",", clases_simples[i], ".\n", clases_simples[i].distances)


#valids = graphs.getValidClasses(estudiantes)
#posibles_distancias = graphs.analizeDistances(valids, distancias)
#for i in posibles_distancias.keys():
#    print(i)
#    print(posibles_distancias[i])
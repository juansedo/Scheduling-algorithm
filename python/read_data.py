import time
import csv
import inits
from pathlib import Path
import graphs

start_time = time.time()

aulas = inits.aulasInit()
estudiantes = inits.estudiantesInit()
clases = inits.clasesInit(aulas)
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

        reg +=len(map_of_clases[id_clase])
    line_count += 1
  print(f'mat20192 file: Processed {line_count} lines ({reg} registered).')

clases_simples = inits.clasesSimplesInit(estudiantes)
clases_simples.sort(key=lambda x: (int(x.impairment), x.numberOfStudents))

for clase in clases_simples:
    graphs.AssignRooms(clase, distancias, aulas)
"""
def findClassrooms(aulas, distancias, clases_simples, clase):
  if clase is None or len(clase.arrivals.keys()) == 0:
    return
  zeroCount = set([])
  dist_totales = []
  for b in distancias.keys():
    if b == 28: continue
    total = 0
    for arrival in clase.arrivals.values():
      if arrival[0].block() == 0:
        findClassrooms(aulas, distancias, clases_simples, arrival)
        if arrival.block == 0: zeroCount.add(arrival)
        continue
      elif distancias[b].get(arrival.block) is None:
        continue
      total += arrival.amount * distancias[b][arrival.block]
    if clase.room != 0: total += distancias[b][(clase.room // 1000)]
    dist_totales.append([b, total])
  clase.distances = sorted(dist_totales, key= lambda elem: elem[1])

  print(clase)
  for dist in clase.distances:
    if clase.room != 0 and not zeroCount: return
    if aulas.get(dist[0]) is None: continue

    possible_rooms = [x for x in aulas[dist[0]].keys() if graphs.checkAvailability(aulas[dist[0]][x], clase)]
    if not possible_rooms: continue

    if clase.room == 0:
        clase.room = possible_rooms.pop()
        aulas[dist[0]][clase.room].availability[clase.day].append([clase.start_time+"-"+clase.end_time])

    zeroCount_copy = zeroCount.copy()

    for arrival_zero in zeroCount_copy:
      if not possible_rooms: break
      arrival_room = possible_rooms.pop()
      clases_simples[arrival_zero.id].room = arrival_room
      clase.arrivals[arrival_zero.id].block = dist[0]
      aulas[dist[0]][arrival_room].available = False
      zeroCount.remove(arrival_zero)

for i in clases_simples:
  findClassrooms(aulas, distancias, clases_simples, i)

for i in clases_simples:
  print(i, ".\n", i.distances)
"""


print("--- %s seconds ---" % (time.time() - start_time))

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

        reg +=len(map_of_clases[id_clase])
    line_count += 1
  print(f'mat20192 file: Processed {line_count} lines ({reg} registered).')
  for clase in clases:
      try:
          a = aulas[clases.bloque()][clases.room]
      except:
          clases.remove(clase)
clases = [x for x in clases if x.numberOfStudents > 0 and x.room != 0]
clases_simples = inits.clasesSimplesInit(estudiantes)
clases_simples = [x for x in clases_simples if x.numberOfStudents > 0 and x.room != 0]

for clase in clases_simples:
    print(clase.room)

print("old distance= " + str(graphs.calcDistances(clases_simples, distancias)))
inits.initAvailabilities(clases, aulas)
clases_simples.sort(key=lambda x: (int(x.impairment), x.numberOfStudents))

for clase in clases_simples:
    graphs.AssignRooms(clase, distancias, aulas)

for clase in clases_simples:
    print(clase.room)

print("new distance= " + str(graphs.calcDistances(clases_simples, distancias)))
print("--- %s seconds ---" % (time.time() - start_time))

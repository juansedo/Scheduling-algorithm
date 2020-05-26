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
  print(f'Processed {line_count} lines ({reg} registered).')

valids = graphs.getValidClasses(estudiantes)
for valid in valids:
    print("* "+valid.code + " " +str(graphs.analizeDistances(valid, 30, distancias)))
    for clase in valid.arrival_classes:
        print(clase.code + " " + clase.group + ": " + str(valid.arrival_students[clase.id]))

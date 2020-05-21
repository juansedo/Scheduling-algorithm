import csv
import inits
from pathlib import Path
import graphs

def clasesById(clases, class_id, group):
  set_class = set([])
  for cl in clases:
    if cl.code == class_id and cl.group == group:
      set_class.add(cl)
  return set_class

aulas = inits.aulasInit()
estudiantes = inits.estudiantesInit()
clases = inits.clasesInit()

path = Path(__file__).parent / "mat20192.csv"
with open(path, encoding="utf8") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  reg = 0
  clases = []
  for row in csv_reader:
    if estudiantes.get(row[0]) is not None:
      estudiantes[row[0]].addClass(clasesById(clases, row[1], row[2]))
      reg +=1
    line_count += 1
  print(f'Processed {line_count} lines ({reg} registered).')

#graphs.createGraph(estudiantes)

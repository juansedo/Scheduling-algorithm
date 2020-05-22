import csv
from pathlib import Path

class Clase:
  def __init__(self, line):
    self.code = line[0]
    self.group = int(line[1])
    self.teacher = line[2]
    self.day = line[3]
    self.start_time = line[4]
    self.end_time = line[5]
    self.room = line[6]

  def __repr__(self):
    return f'<%s, %s, %s>' % (self.code, self.group, self.day)

class Aula:
  def __init__(self, line):
    self.id = line[0]
    self.tipo = line[1]
    self.capacidad = line[2]
    self.accesible = line[3] == "1"

  def __str__(self):
    return self.id + ", " + self.tipo + "\n"

class Estudiante:
  def __init__(self, line):
    self.code = line[0]
    self.inpairment = line[1] == "1"
    self.days = {'L' : [], 'M' : [], 'W' : [], 'J' : [], 'V' : [], 'S' : [], 'D' : []}

  def addClass(self, classrooms):
    for cl in classrooms:
      switcher = {"lunes": 'L', "martes": 'M',
                  "miércoles": 'W', "jueves": 'J',
                  "viernes": 'V', "sábado": 'S',
                  "domingo": 'D'
      }
      self.days[switcher.get(cl.day)].append(cl)

def aulasInit():
  path = Path(__file__).parent / "aulas.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    aulas = []
    for row in csv_reader:
      aulas.append(Aula(row))
      line_count += 1
    print(f'Processed {line_count} lines.')
  return aulas

def estudiantesInit():
  path = Path(__file__).parent / "estudiantes.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    estudiantes = {}
    for row in csv_reader:
      estudiantes[row[0]] = Estudiante(row)
      line_count += 1
    print(f'Processed {line_count} lines.')
  return estudiantes

def distanciasInit():
  path = Path(__file__).parent / "DistanciasBloques.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    distancias = {}
    for row in csv_reader:
      b1 = int(row[0])
      b2 = int(row[1])
      dist = int(row[2])
      if distancias.get(b1) is None:
        distancias[b1] = {}
      if distancias.get(b2) is None:
        distancias[b2] = {}
      distancias[b1][b2] = dist
      distancias[b2][b1] = dist
      line_count += 1
    print(f'Processed {line_count} lines.')
  return distancias

def clasesInit():
  path = Path(__file__).parent / "pa20192.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    clases = []
    for row in csv_reader:
      clases.append(Clase(row))
      line_count += 1
    print(f'Processed {line_count} lines.')
  return clases

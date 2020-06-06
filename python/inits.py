import csv
from pathlib import Path

class Clase:
  def __init__(self, line):
    switcher = {
      "lunes": 'L', "martes": 'M',
       "miércoles": 'W', "jueves": 'J',
       "viernes": 'V', "sábado": 'S',
       "domingo": 'D'
    }
    self.code = line[0]
    self.group = line[1]
    self.teacher = line[2]
    self.day = switcher.get(line[3])
    self.start_time = line[4]
    self.end_time = line[5]
    self.room = int(line[6])
    self.impairment = False
    self.numberOfStudents = 0
    self.id = f'<%s.%s.%s>' % (self.code, self.group, self.day)
    self.arrivals = {}

  def block(self):
      return self.room // 1000

  def addArrival(self, clase):
    if self.arrivals.get(clase.id) is None:
      self.arrivals[clase.id] = Arrival(clase, 0)
    self.arrivals[clase.id].amount += 1

  def __repr__(self):
    return f'<%s.%s.%s>' % (self.code, self.group, self.day)

def clasesInit(aulas):
  path = Path(__file__).parent / "pa20192.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    clases = []
    for row in csv_reader:
      block = int(row[6]) // 1000
      clases.append(Clase(row))
      line_count += 1
    print(f'pa20192: Processed {line_count} lines.')
  return clases

def clasesSimplesInit(estudiantes):
  clases = []
  for est in estudiantes.values():
    for day in est.days.keys():
      for c_desde in est.days[day]:
        for c_hasta in est.days[day]:
          if c_desde.code != c_hasta.code and c_desde.end_time == c_hasta.start_time:
            if c_hasta not in clases:
              clases.append(c_hasta)
            c_hasta.addArrival(c_desde)
  return clases

class Aula:
  def __init__(self, line):
    self.id = int(line[0])
    self.desc = line[1]
    self.capacity = line[2] if line[2] != "N/A" else 1000
    self.access = line[3] == "1"
    self.availability = {'L' : [], 'M' : [], 'W' : [], 'J' : [], 'V' : [], 'S' : [], 'D' : []}


def aulasInit():
  path = Path(__file__).parent / "aulas.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    aulas = {}
    for row in csv_reader:
      i = int(row[0])
      b = i // 1000
      if aulas.get(b) is None:
        aulas[b] = {}
      aulas[b][i] = Aula(row)
      line_count += 1
    print(f'aulas: Processed {line_count} lines.')
  return aulas

class Estudiante:
  def __init__(self, line):
    self.code = line[0]
    self.impairment = line[1] == "1"
    self.days = {'L' : [], 'M' : [], 'W' : [], 'J' : [], 'V' : [], 'S' : [], 'D' : []}

  def addClass(self, classrooms):
    for cl in classrooms:
      self.days[cl.day].append(cl)
      cl.numberOfStudents += 1
      cl.impairment = cl.impairment or self.impairment

def estudiantesInit():
  path = Path(__file__).parent / "estudiantes.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    estudiantes = {}
    for row in csv_reader:
      estudiantes[row[0]] = Estudiante(row)
      line_count += 1
    print(f'estudiantes: Processed {line_count} lines.')
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
        distancias[b1][b1] = 0
      if distancias.get(b2) is None:
        distancias[b2] = {}
        distancias[b2][b2] = 0
      distancias[b1][b2] = dist
      distancias[b2][b1] = dist
      line_count += 1
    print(f'DistanciaBloques: Processed {line_count} lines.')
  return distancias


def mappingClases(clases):
  out = {}
  for cl in clases:
    cl_id = str(cl.code) + "." + str(cl.group)
    if out.get(cl_id) is None:
      out[cl_id] = set([])
    out[cl_id].add(cl)
  return out

def initAvailabilities(clases, aulas):
    for clasex in clases:
        block = clasex.block()
        if aulas.get(block) is not None and aulas[block].get(clasex.room) is not None:
            aulas[block][clasex.room].availability[clasex.day].append(clasex.start_time+"-"+clasex.end_time)

class Arrival:
  """
    Representa una clase del conjunto arrival. Permite saber cuántos estudiantes
    vienen por cada clase

    Atributos
    ----------
    clase : Clase
      Representa una clase
    amount : int
      Cantidad de estudiantes que vienen de esa clase
  """
  def __init__(self, clase, amount):
    self.clase = clase
    self.amount = amount

  def _repr_(self):
    return f'(id:%s, t:%s)' % (self.clase._repr_(), self.amount)

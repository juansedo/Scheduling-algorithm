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
    self.id = f'<%s.%s.%s>' % (self.code, self.group, self.day)
    
  def __repr__(self):
    return f'<%s.%s.%s>' % (self.code, self.group, self.day)

class Arrival:
  def __init__(self, clase, block, amount):
    self.id = clase
    self.block = block
    self.amount = amount

  def __repr__(self):
    return f'(id:%s, b:%s, t:%s)' % (self.id, self.block, self.amount)

class ClaseSimpleInfo:
  def __init__(self, room):
    self.arrivals = {}
    self.distances = []
    self.room = room
    self.visited = False

  def addArrival(self, clase):
    if self.arrivals.get(clase.id) is None:
      self.arrivals[clase.id] = Arrival(clase.id, clase.room//1000, 0)
    self.arrivals[clase.id].amount += 1

  def __repr__(self):
    return f'(r:%s, arr:%s)' % (self.room, self.arrivals)

def clasesInit(aulas):
  path = Path(__file__).parent / "pa20192.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    clases = []
    for row in csv_reader:
      block = int(row[6]) // 1000
      #if aulas.get(block) is not None and aulas[block].get(row[6]) is not None:
      #  aulas[block][row[6]].available = False
      clases.append(Clase(row))
      line_count += 1
    print(f'pa20192: Processed {line_count} lines.')
  return clases

def clasesSimplesInit(estudiantes):
  clases = {}
  for est in estudiantes.values():
    for day in est.days.keys():
      for c_desde in est.days[day]:
        for c_hasta in est.days[day]:
          if c_desde.id != c_hasta.id and c_desde.end_time == c_hasta.start_time:
            if clases.get(c_hasta.id) is None:
              clases[c_hasta.id] = ClaseSimpleInfo(c_hasta.room)
            clases[c_hasta.id].addArrival(c_desde)
          
          if c_hasta.room == 0:
            if clases.get(c_hasta.id) is None:
              clases[c_hasta.id] = ClaseSimpleInfo(c_hasta.room)
          
          if c_desde.room == 0:
            if clases.get(c_desde) is None:
              clases[c_desde.id] = ClaseSimpleInfo(c_desde.room)
  return clases

class Aula:
  def __init__(self, line):
    self.id = int(line[0])
    self.desc = line[1]
    self.capacity = line[2]
    self.access = line[3] == "1"
    self.available = True

  def __str__(self):
    return self.id + ", " + self.tipo + "\n"

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
    self.inpairment = line[1] == "1"
    self.days = {'L' : [], 'M' : [], 'W' : [], 'J' : [], 'V' : [], 'S' : [], 'D' : []}

  def addClass(self, classrooms):
    for cl in classrooms:
      self.days[cl.day].append(cl)

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
import csv
from pathlib import Path

class Clase:
  """
    Representa una clase agendada o por agendar del archivo pa20192.csv

    Atributos
    ----------
    code : str
      Código de la clase
    group : str
      Número del grupo
    teacher : str
      Identificación del profesor
    day : str {'L', 'M', 'W', 'J', 'V', 'S', 'D'}
      El día en que se da la clase
    start_time : str
      Hora de inicio de la clase
    end_time : str
      Hora de finalización de la clase
    room : int
      Número de salón de clase
    impairment : bool
      True si la clase tiene algún discapacitado fisico
    numberOfStudents : int
      Cantidad de estudiantes que recibirá la clase
    arrivals : {str: Arrival}
      Conjunto con las clases que le llegan a esta clase. Es
      decir, están inmediatamente antes de esta y tienen 
      estudiantes en común.

    Métodos
    -------
    addArrival(clase)
      Añade una clase a la lista de arrivals
    
    getBlock()
      Obtiene el bloque en el que se encuentra la clase
      actualmente.

    getSchedule()
      Obtiene el horario en el que se encuentra la clase
      actualmente.
      Formato: HORA_INICIO-HORA_FIN
  """
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
    self.arrivals = {}
  
  def addArrival(self, clase):
    if self.arrivals.get(clase.__repr__()) is None:
      self.arrivals[clase.__repr__()] = Arrival(clase, 0)
    self.arrivals[clase.__repr__()].amount += 1

  def getBlock(self):
    return self.room // 1000
  
  def getSchedule(self):
    return self.start_time + "-" + self.end_time
  
  def __repr__(self):
    return f'<%s.%s.%s>' % (self.code, self.group, self.day)


class Arrival:
  """
    Representa una clase del diccionario arrivals (ver Clase). Permite saber
    cuántos estudiantes vienen por cada clase

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

"""
clasesInit()
  Inicializa una lista de clases recogidas de un csv
"""
def clasesInit():
  path = Path(__file__).parent / "pa20192.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    clases = [Clase(row) for row in csv_reader]
    line_count = len(clases)
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
  """
    Representa un aula de clase de la universidad

    Atributos
    ----------
    id : int
      Es el código del salón. Es int para poder
      definir el bloque a partir de este
    desc: str
      Descripción del salón
    capacity : int
      Cantidad de estudiantes
    access : bool
      True si es accesible para discapacitados
    availability : {str:[str]}
      Diccionario con la información de los 
      horarios en los que no se encuentra disponible
      el salón
  """
  def __init__(self, line):
    self.id = int(line[0])
    self.desc = line[1]
    self.capacity = line[2] if line[2] != "N/A" else 1000
    self.access = line[3] == "1"
    self.availability = {'L' : [], 'M' : [], 'W' : [], 'J' : [], 'V' : [], 'S' : [], 'D' : []}

"""
aulasInit()
  Inicializa una lista de salones recogidos de un csv
"""
def aulasInit():
  path = Path(__file__).parent / "aulas.csv"
  with open(path, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    aulas = {}
    for row in csv_reader:
      room = int(row[0])
      block = room // 1000
      if aulas.get(block) is None:
        aulas[block] = {}
      aulas[block][room] = Aula(row)
      line_count += 1
    print(f'aulas: Processed {line_count} lines.')
  return aulas

class Estudiante:
  """
    Representa a un estudiante del archivo estudiantes.csv

    Atributos
    ----------
    code : str
      Es el código del estudiante
    impairment : bool
      Indica si el estudiante tiene alguna discapacidad
    days : {str: [Clase]}
      Diccionario con la lista de clases que un
      estudiantes tiene cada día

    Métodos
    -------
    addClass(classrooms)
      Recibe un conjunto de clases y las agrega al
      estudiante según el día
  """
  def __init__(self, line):
    self.code = line[0]
    self.impairment = line[1] == "1"
    self.days = {'L' : [], 'M' : [], 'W' : [], 'J' : [], 'V' : [], 'S' : [], 'D' : []}

  def addClass(self, classrooms):
    for cl in classrooms:
      self.days[cl.day].append(cl)
      cl.numberOfStudents += 1
      cl.impairment = cl.impairment or self.impairment

"""
estudiantesInit()
  Inicializa un diccionario de los estudiantes recogidos de un csv
"""
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


"""
distanciasInit()
  Inicializa un diccionario de las distancias entre bloques recogidas de un csv
"""
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

"""
mappingClases(clases)
  Recibe una lista de clases y devuelve un diccionario que
  organiza clases de mismo código y grupo por CÓDIGO.GRUPO
  Así, si un estudiante se matriculó en ABC.10, en el
  diccionario se guardarán todas los días que tiene clases
  con esa materia 
"""
def mappingClases(clases):
  out = {}
  for cl in clases:
    cl_id = str(cl.code) + "." + str(cl.group)
    if out.get(cl_id) is None:
      out[cl_id] = set([])
    out[cl_id].add(cl)
  return out

"""
initAvailabilities()
  Inicializa los horarios de las aulas
"""
def initAvailabilities(clases, aulas):
    for cl in clases:
        block = cl.getBlock()
        if aulas.get(block) is not None and aulas[block].get(cl.room) is not None:
            aulas[block][cl.room].availability[cl.day].append(cl.getSchedule())
from inits import Arrival
import inits

def analizeSubDistances(clase, distancias, assigneds):
  if len(assigneds) == 0:
    return distancias.keys()
  distancias_totales = []
  for bloque in distancias.keys():
    if bloque in [0, 21, 28, 31]: #[0, 7, 13, 14, 15, 16, 17, 18, 19, 21, 23, 26, 27, 28, 29, 30, 31, 33, 34, 35, 38]:
      continue
    distancia = 0
    for assigned in assigneds:
      if assigned.clase.getBlock() != -1:
        distancia += assigned.amount * distancias[int(bloque)][assigned.clase.getBlock()]
      else:
        distancia = -1
        break
    if len(distancias_totales) == 0:
      distancias_totales.append((bloque, distancia))
    else:
      for i in range(len(distancias_totales)):
        if distancia < distancias_totales[i][1]:
          distancias_totales.insert(i, (bloque, distancia))
          break
        elif i == len(distancias_totales) - 1:
          distancias_totales.append( (bloque, distancia))
  return [x[0] for x in distancias_totales]

def analizeBestDistances(arrivals, distancias):
  distancias_totales = []
  for bloque in distancias.keys():
    if bloque in [0, 21, 28, 31]:
      continue
    distancia = sum([arv.amount * distancias[int(bloque)][arv.clase.getBlock()] for arv in arrivals if arv.clase.getBlock() != -1])
    distancias_totales.append((bloque, distancia))
  return dict(sorted(distancias_totales, key=lambda elem: elem[1])).keys()

def checkAvailability(clase, room):
    available = ((not clase.impairment) or room.access) and clase.numberOfStudents <= int(room.capacity)
    if not available:
        return False
    for time_lapse in room.availability[clase.day]:
        time_lapse = time_lapse.split("-")
        available = available and not tti(time_lapse[0]) <= tti(clase.start_time) < tti(time_lapse[1])
        available = available and not tti(time_lapse[0]) < tti(clase.end_time) <= tti(time_lapse[1])
        available = available and not(tti(time_lapse[0]) > tti(clase.start_time) and tti(time_lapse[1]) < tti(clase.end_time))
    return available

def tti(hora): #Time to int
  return int("".join(hora.split(":")))

def AssignBestRoom(clase, aulas, distancias, conexiones):
  #bests = analizeSubDistances(clase, distancias, conexiones)
  bests = analizeBestDistances(clase.arrivals.values(), distancias)
  for bloque in bests:
    if bloque == clase.getBlock():
      return
    for aula in aulas[bloque].values():
      if checkAvailability(clase, aula):
        if clase.room == 14204 or clase.getBlock() == -1:
          return
        if (clase.getSchedule()) in aulas[clase.getBlock()][clase.room].availability[clase.day]:
          aulas[clase.getBlock()][clase.room].availability[clase.day].remove(clase.getSchedule())
        aula.availability[clase.day].append(clase.getSchedule())
        clase.room = aula.id
        return
  print("estamos es pero en la olla manito")

def AssignRooms(arrivedClase, distancias, aulas):
  for arrival in arrivedClase.arrivals.values():
    if len(arrival.clase.arrivals) == 0:
      AssignBestRoom(arrival.clase, aulas, distancias, getAssigneds(arrivedClase, arrival))
    else:
      AssignRooms(arrival.clase, distancias, aulas)
      AssignBestRoom(arrival.clase, aulas, distancias, getAssigneds(arrivedClase, arrival) + list(arrival.clase.arrivals.values()))
  AssignBestRoom(arrivedClase, aulas, distancias, arrivedClase.arrivals.values())

"""
getAssigneds()
  Enlista los salones ya asignados, que son arrivals de la arrivedClase
  distintos al receptor y agrega a la misma clase con el total de receptor
"""
def getAssigneds(claseSimple, receptor):
  assigned = [arv for arv in claseSimple.arrivals.values() if arv != receptor]
  assigned.append(Arrival(claseSimple, receptor.amount))
  return assigned

"""
calcDistances()
  Calcula la distancia total que se recorre en los desplazamientos entre clases
"""
def calcDistances(clases, distancias):
  distancia = 0
  for clase in clases:
    for arrival in clase.arrivals.values():
      if clase.getBlock() != -1 and arrival.clase.getBlock() != -1:
        distancia += arrival.amount * distancias[clase.getBlock()][arrival.clase.getBlock()]
  return distancia

"""
print_comparison()
  Imprime una comparación de las listas de clases antes y después
"""
def print_comparison(distancias, old, new):
  print("Before...\t\t\t\tNow...")
  for k in new.keys():
    print(old[k],":", old[k].room,"(",old[k].getSchedule(),")",end='\t\t\t')
    print(new[k],":", new[k].room,"(",new[k].getSchedule(),")")
  print("TOTAL DISTANCE :", str(calcDistances(old.values(), distancias)), end='\t\t\t')
  print("TOTAL DISTANCE :", str(calcDistances(new.values(), distancias)))
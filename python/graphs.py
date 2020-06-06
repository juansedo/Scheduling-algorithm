from inits import Arrival
import inits

def analizeSubDistances(clase, distancias, assigneds):
  if len(assigneds) == 0:
    return distancias.keys()
  distancias_totales = []
  for bloque in distancias.keys():
    if bloque in [0, 13, 21, 28, 31]:
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

"""
checkAvailability()
  Comprueba si no hay colisiones en un día determinado para cierto room con
  el horario de la clase
"""
def checkAvailability(clase, room):
    if (clase.impairment and not(room.access)) or clase.numberOfStudents > int(room.capacity):
        return False
    return all([checkTimeCollision(t, clase.getSchedule()) for t in room.availability[clase.day]])

"""
checkTimeCollision(time1, time2)
  Comprueba si, en cierto sentido, los tiempos dados en el formato 9:00-16:00
  colisionan
"""
def checkTimeCollision(time1, time2):
  time1 = time1.split("-")
  time2 = time2.split("-")
  time1 = {'start': int("".join(time1[0].split(":"))), 'end': int("".join(time1[1].split(":")))}
  time2 = {'start': int("".join(time2[0].split(":"))), 'end': int("".join(time2[1].split(":")))}
  return (time2['end'] <= time1['start'] or time1['end'] <= time2['start'])

def AssignBestRoom(clase, aulas, distancias, conexiones):
  bests = analizeSubDistances(clase, distancias, conexiones)
  #bests = analizeBestDistances(clase.arrivals.values(), distancias)
  for bloque in bests:
    if bloque == clase.getBlock():
      return
    for aula in aulas[bloque].values():
      if checkAvailability(clase, aula):
        if clase.getBlock() == -1:
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
  assigned = []
  for arv in claseSimple.arrivals.values():
      if arv != receptor:
          assigned.append(arv)
      else:
          break
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
  def formatNumber(num):
    return "0" + str(num) if int(num) < 10000 else num
  print("BEFORE...\t\t\t\t\tNOW...")
  for k in new.keys():
    print(old[k],":", formatNumber(old[k].room),"(",old[k].getSchedule(),")",end='\t')
    print(new[k],":", formatNumber(new[k].room),"(",new[k].getSchedule(),")")
  print("TOTAL DISTANCE :", str(calcDistances(old.values(), distancias)), end='\t\t\t\t')
  print("TOTAL DISTANCE :", str(calcDistances(new.values(), distancias)))

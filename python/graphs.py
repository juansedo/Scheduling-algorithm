import inits

def getValidClasses(estudiantes):
    valids = []
    for estudiante in estudiantes.values():
        for day in estudiante.days.keys():
            for clase_desde in estudiante.days[day]:
                for clase_hasta in estudiante.days[day]:
                    if int(clase_hasta.room) != 0:
                        continue
                    if clase_desde.end_time == clase_hasta.start_time and clase_hasta.code+"."+str(clase_hasta.group) != clase_desde.code+"."+str(clase_desde.group):
                        if clase_hasta not in valids:
                            valids.append(clase_hasta)
                        if clase_desde not in clase_hasta.arrival_classes:
                            clase_hasta.arrival_classes.append(clase_desde)
                        try:
                            clase_hasta.arrival_students[clase_desde.id] += 1
                        except:
                            clase_hasta.arrival_students[clase_desde.id] = 1
    return valids

def analizeDistances(valids, distancias):
    distancias_totales = {}
    for valid in valids:
        distancias_totales[valid.id] = []
        for bloque in distancias.keys():
            if bloque == "28":
                continue
            distancia = 0
            for clase in valid.arrival_classes:
                if int(clase.room[:2]) != 0 and clase.room[:2] != "28":
                    print(distancias[int(bloque)][int(clase.room[:2])])
                    distancia += valid.arrival_students[clase.id] * distancias[int(bloque)][int(clase.room[:2])]
                else:
                    distancia = -1
                    break
            if len(distancias_totales[valid.id]) == 0:
                distancias_totales[valid.id].append((bloque, distancia))
            else:
                for i in range(len(distancias_totales[valid.id])):
                    if distancia < distancias_totales[valid.id][i][1]:
                        distancias_totales[valid.id].insert(i, (bloque, distancia))
                        break
                    elif i == len(distancias_totales[valid.id]) - 1:
                        distancias_totales[valid.id].append( (bloque, distancia))
    return distancias_totales

def getTotalDistances(distances, clase):
  total = {}
  for bloque in distances.keys():
    total[bloque] = 0
    for i in clase.arrivals.keys():
      total[bloque] += clase.arrivals[i] * distances[bloque][clase.arrivals[i]]
  return total


def checkAvailability(room, clase):
    available = not (clase.impairment and (not room.impairment) or clase.numberOfStudents < int(room.capacity))
    if not available:
        return False
    for time_lapse in room.availability[clase.day]:
        time_lapse = time_lapse.split("-")
        available = available and not (tti(time_lapse[0]) < tti(room.start_time) < tti(time_lapse[0]) or tti(time_lapse[0]) < tti(room.end_time) < tti(time_lapse[0]))
    return available
def tti(hora): #Time to int
    return int("".join(hora.split(":")))

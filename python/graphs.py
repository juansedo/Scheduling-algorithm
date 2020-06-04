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

def analizeSubDistances(clase, distancias, assigneds):
    if len(assigneds) == 0:
        return distancias.keys()
    distancias_totales = []
    for bloque in distancias.keys():
        if bloque == 28 or bloque == 31:
            continue
        distancia = 0
        for arrival in assigneds:
            if arrival[0].block() != 0 and arrival[0].block() != 28 and arrival[0].block() != 31:
                distancia += arrival[1] * distancias[int(bloque)][arrival[0].block()]
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

def checkAvailability(clase, room):
    available =  ((not clase.impairment) or room.access) and clase.numberOfStudents >= int(room.capacity)
    if not available:
        return False
    for time_lapse in room.availability[clase.day]:
        time_lapse = time_lapse.split("-")
        available = available and not (tti(time_lapse[0]) < tti(clase.start_time) < tti(time_lapse[0]) or tti(time_lapse[0]) < tti(clase.end_time) < tti(time_lapse[0]))
    return available
def tti(hora): #Time to int
    return int("".join(hora.split(":")))


def getAssigneds(claseSimple, receptor):
    assigned = []
    for clase in claseSimple.arrivals.values():
        if int(clase[0].room) != 0:
            assigned.append(clase)
        else:
            continue
    if claseSimple.block() != 0:
        assigned.append([claseSimple, receptor[1]])
    return assigned

def AssignBestRoom(clase, aulas, distancias, conexiones):
    if len(conexiones) == 0:
        bests = analizeSubDistances(clase, distancias, clase.arrivals.values())
    else:
        bests = analizeSubDistances(clase, distancias, conexiones)
    for bloque in bests:
        for aula in aulas[bloque].keys():
            if checkAvailability(clase, aulas[bloque][aula]):
                aulas[bloque][aula].availability[clase.day].append(clase.start_time+"-"+clase.end_time)
                return
    print("estamos es pero en la olla manito")


def AssignRooms(claseSimple, distancias, aulas):
    for clase in claseSimple.arrivals.values():
        if len(clase[0].arrivals) == 0:
            AssignBestRoom(clase[0], aulas, distancias, getAssigneds(claseSimple, clase))
        else:
            AssignRooms(clase[0], distancias, aulas)
            AssignBestRoom(clase[0], aulas, distancias, [])
    AssignBestRoom(claseSimple, aulas, distancias, [])

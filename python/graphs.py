import inits

def analizeSubDistances(clase, distancias, assigneds):
    if len(assigneds) == 0:
        return distancias.keys()
    distancias_totales = []
    for bloque in distancias.keys():
        if bloque == 28 or bloque == 31:
            continue
        distancia = 0
        for arrival in assigneds:
            if arrival[0].block() != 0 and arrival[0].block() != 28 and arrival[0].block() != 31 and arrival[0].block() != 21:
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
    available =  ((not clase.impairment) or room.access) and clase.numberOfStudents <= int(room.capacity)
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


def getAssigneds(claseSimple, receptor):
    assigned = []
    for clase in claseSimple.arrivals.values():
        if clase[0].room != 0:
            assigned.append(clase)
    if claseSimple.room != 0:
        assigned.append([claseSimple, receptor[1]])
    return assigned

def AssignBestRoom(clase, aulas, distancias, conexiones):
    if clase.room != 0:
        return
    bests = analizeSubDistances(clase, distancias, conexiones)
    for bloque in bests:
        for aula in aulas[bloque].values():
            if checkAvailability(clase, aula):
                aula.availability[clase.day].append(clase.start_time+"-"+clase.end_time)
                clase.room = aula.id
                return
    print("estamos es pero en la olla manito")


def AssignRooms(claseSimple, distancias, aulas):
    for clase in claseSimple.arrivals.values():
        if clase[0].room != 0:
            continue
        if len(clase[0].arrivals) == 0:
            AssignBestRoom(clase[0], aulas, distancias, getAssigneds(claseSimple, clase))
        else:
            AssignRooms(clase[0], distancias, aulas)
            AssignBestRoom(clase[0], aulas, distancias, getAssigneds(claseSimple, clase) + list(clase[0].arrivals.values()))

    if claseSimple.room == 0:
        AssignBestRoom(claseSimple, aulas, distancias, claseSimple.arrivals.values())

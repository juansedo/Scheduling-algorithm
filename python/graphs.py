from inits import Arrival
import inits

def analizeSubDistances(clase, distancias, assigneds):
    if len(assigneds) == 0:
        return distancias.keys()
    distancias_totales = []
    for bloque in distancias.keys():
        if bloque == 28 or bloque == 31:
            continue
        distancia = 0
        for assigned in assigneds:
            if assigned.clase.block() != 0 and assigned.clase.block() != 28 and assigned.clase.block() != 31 and assigned.clase.block() != 21:
                distancia += assigned.amount * distancias[int(bloque)][assigned.clase.block()]
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
    for arrival in claseSimple.arrivals.values():
        if arrival != receptor:
            assigned.append(arrival)
    assigned.append(Arrival(claseSimple, receptor.amount))
    return assigned

def AssignBestRoom(clase, aulas, distancias, conexiones):
    if clase.room == 0:
        return
    bests = analizeSubDistances(clase, distancias, conexiones)
    for bloque in bests:
        if bloque == clase.block():
            return
        for aula in aulas[bloque].values():
            if checkAvailability(clase, aula):
                if clase.room == 14204:
                    return
                if (clase.start_time+"-"+clase.end_time) in aulas[clase.block()][clase.room].availability[clase.day]:
                    aulas[clase.block()][clase.room].availability[clase.day].remove(clase.start_time+"-"+clase.end_time)
                aula.availability[clase.day].append(clase.start_time+"-"+clase.end_time)
                clase.room = aula.id
                return
    print("estamos es pero en la olla manito")


def AssignRooms(claseSimple, distancias, aulas):
    for arrival in claseSimple.arrivals.values():
        if len(arrival.clase.arrivals) == 0:
            AssignBestRoom(arrival.clase, aulas, distancias, getAssigneds(claseSimple, arrival))
        else:
            AssignRooms(arrival.clase, distancias, aulas)
            AssignBestRoom(arrival.clase, aulas, distancias, getAssigneds(claseSimple, arrival) + list(arrival.clase.arrivals.values()))

    AssignBestRoom(claseSimple, aulas, distancias, claseSimple.arrivals.values())

def calcDistances(clases, distancias):
    distancia = 0
    for clase in clases:
        for arrival in clase.arrivals.values():
            if clase.block() == 0 or arrival.clase.block() == 0 or clase.block() == 28 or arrival.clase.block() == 28:
                continue
            distancia += arrival.amount * distancias[clase.block()][arrival.clase.block()]
    return distancia

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



def analizeDistances(valid, bloque, distancias):
    distancia = 0
    for clase in valid.arrival_classes:
        if int(clase.room[:2]) != 0:
            distancia += valid.arrival_students[clase.id] * distancias[bloque][int(clase.room[:2])]
        else:
            return -1
    return distancia

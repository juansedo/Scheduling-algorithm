def createGraph(estudiantes):
    graph = {"L": {}, "M": {}, "W": {}, "J": {}, "V": {}, "S": {}, "D": {}}
    for estudiante in estudiantes.values():
        for day in estudiante.days.keys():
            for clase_desde in estudiante.days[day]:
                for clase_hasta in estudiante.days[day]:
                    if clase_desde.end_time == clase_hasta.start_time:
                        try:
                            try:
                                graph[day][clase_hasta.code+str(clase_hasta.group)][clase_desde.code+str(clase_desde.group)] += 1
                            except:
                                graph[day][clase_hasta.code+str(clase_hasta.group)][clase_desde.code+str(clase_desde.group)] = 1
                        except:
                            graph[day][clase_hasta.code+str(clase_hasta.group)] = {}
                            graph[day][clase_hasta.code+str(clase_hasta.group)][clase_desde.code+str(clase_desde.group)] = 1
    print(graph)

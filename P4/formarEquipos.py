

def generar_todas_las_soluciones(participantes_libres, matriz_conflictos):
    # Si no quedan participantes, hemos completado una formación válida
    if not participantes_libres:
        return 0  # Retornamos 0 para ir sumando los conflictos en la recursión

    # Para evitar soluciones duplicadas, fijamos el primer participante disponible
    p1 = participantes_libres[0]
    resto_tras_p1 = participantes_libres[1:]
    
    min_conflicto_total = float('inf')

    # Buscamos todas las parejas posibles (p2, p3) para acompañar a p1
    for i in range(len(resto_tras_p1)):
        for j in range(i + 1, len(resto_tras_p1)):
            p2 = resto_tras_p1[i]
            p3 = resto_tras_p1[j]

            # Calculamos el conflicto de este equipo específico de 3
            # Recuerda que c_ij no siempre es igual a c_ji [cite: 42, 43]
            conflicto_equipo = (
                matriz_conflictos[p1][p2] + matriz_conflictos[p1][p3] +
                matriz_conflictos[p2][p1] + matriz_conflictos[p2][p3] +
                matriz_conflictos[p3][p1] + matriz_conflictos[p3][p2]
            )

            # Creamos la lista de participantes que quedan para los siguientes equipos
            nuevos_libres = [p for p in resto_tras_p1 if p != p2 and p != p3]
            
            # Llamada recursiva para formar el resto de los equipos
            resultado_recursivo = generar_todas_las_soluciones(nuevos_libres, matriz_conflictos)
            
            # El conflicto total de esta rama es el de este equipo + el de los siguientes
            conflicto_total = conflicto_equipo + resultado_recursivo
            
            # Guardamos la mejor solución encontrada en esta exploración completa
            if conflicto_total < min_conflicto_total:
                min_conflicto_total = conflicto_total

    return min_conflicto_total


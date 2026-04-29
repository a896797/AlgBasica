
import time
import sys


def leer_matrices_entrada(ruta_entrada):
    """Lee una o varias matrices cuadradas en bloques [N + N filas]."""
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        lineas = [linea.strip() for linea in f if linea.strip()]

    if not lineas:
        raise ValueError("El fichero de entrada esta vacio")

    def leer_bloque(tokens, inicio):
        if inicio >= len(tokens):
            raise ValueError("Falta la dimension de la matriz")

        n = int(tokens[inicio])
        if n <= 0:
            raise ValueError("La dimension N debe ser mayor que 0")

        fin = inicio + 1 + n
        if fin > len(tokens):
            raise ValueError("No hay suficientes filas para la matriz indicada")

        matriz = []
        for fila in tokens[inicio + 1:fin]:
            valores = list(map(int, fila.split()))
            if len(valores) != n:
                raise ValueError("Cada fila debe tener exactamente N valores")
            matriz.append(valores)

        return matriz, fin

    matrices = []

    # Formato: bloques consecutivos [N + N filas], sin cabecera de numero de casos.
    idx = 0
    while idx < len(lineas):
        matriz, idx = leer_bloque(lineas, idx)
        matrices.append(matriz)

    return matrices

def media_matriz(matriz):
    """Devuelve la media de todos los elementos de una matriz."""
    if not matriz or not matriz[0]:
        raise ValueError("La matriz no puede estar vacia")

    total = 0
    cantidad = 0

    for fila in matriz:
        for valor in fila:
            total += valor
            cantidad += 1

    return total / cantidad


def generar_todas_las_soluciones(participantes_libres, matriz_conflictos, media):
    nodos_generados = 1

    # Si no quedan participantes, hemos completado una formación válida
    if not participantes_libres:
        return 0, nodos_generados

    if len(participantes_libres) < 3:
        return float("inf"), nodos_generados

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
            
            conflicto_poda = conflicto_equipo + media * len(nuevos_libres)
            if(conflicto_poda >= min_conflicto_total):
                continue  # Poda: no exploramos esta rama si ya supera el mínimo encontrado
            # Llamada recursiva para formar el resto de los equipos
            resultado_recursivo, nodos_hijo = generar_todas_las_soluciones(
                nuevos_libres,
                matriz_conflictos,
                media
            )
            nodos_generados += nodos_hijo
            
            # El conflicto total de esta rama es el de este equipo + el de los siguientes
            conflicto_total = conflicto_equipo + resultado_recursivo 
            # Guardamos la mejor solución encontrada en esta exploración completa
            if conflicto_total < min_conflicto_total:
                min_conflicto_total = conflicto_total

    return min_conflicto_total, nodos_generados


def construir_reporte_resultados(resultados):
    lineas = []
    ancho = 70
    separador = "=" * ancho
    separador_fino = "-" * ancho

    lineas.append(separador)
    lineas.append("RESULTADOS - FORMACION DE EQUIPOS")
    lineas.append(separador)
    lineas.append(f"Total de problemas: {len(resultados)}")
    lineas.append(separador_fino)
    lineas.append(
        f"{'Problema':<10} {'N':>5} {'Tiempo (ms)':>12} {'Nodos':>12} {'Valor optimo':>15}"
    )
    lineas.append(separador_fino)

    for resultado in resultados:
        lineas.append(
            f"{resultado['problema']:<10} {resultado['n']:>5} "
            f"{resultado['tiempo_ms']:>12.3f} {resultado['nodos']:>12} "
            f"{resultado['valor_optimo']:>15}"
        )

    lineas.append(separador)

    return "\n".join(lineas)


def escribir_resultados_salida(ruta_salida, resultados):
    reporte = construir_reporte_resultados(resultados)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(reporte + "\n")

def main(args): 
    if len(args) != 2:
        print("Uso: python formarEquipos.py <archivo_entrada>.txt <archivo_salida>.txt")
        return
    archivo_entrada = args[0]
    archivo_salida = args[1]

    try:
        matrices_conflictos = leer_matrices_entrada(archivo_entrada)
    except (OSError, ValueError) as e:
        print(f"Error al leer el fichero de entrada: {e}")
        return

    resultados = []
    for idx, matriz in enumerate(matrices_conflictos, 1):
        media = media_matriz(matriz)
        participantes = list(range(len(matriz)))

        inicio = time.perf_counter()
        valor_optimo, nodos = generar_todas_las_soluciones(participantes, matriz, media)
        fin = time.perf_counter()

        tiempo_ms = (fin - inicio) * 1000
        resultados.append(
            {
                "problema": idx,
                "n": len(matriz),
                "tiempo_ms": tiempo_ms,
                "nodos": nodos,
                "valor_optimo": valor_optimo,
            }
        )

    print(construir_reporte_resultados(resultados))

    try:
        escribir_resultados_salida(archivo_salida, resultados)
    except OSError as e:
        print(f"Error al escribir el fichero de salida: {e}")

if __name__ == "__main__":  
    main(sys.argv[1:])



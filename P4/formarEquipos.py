import heapq
import itertools
import sys
import time


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


def coste_equipo(matriz, p1, p2, p3):
    """Nivel de conflicto de un equipo {p1, p2, p3}: suma de los conflictos
    de cada participante hacia los otros dos miembros (c_ij no tiene por
    que coincidir con c_ji, asi que se suman ambos sentidos)."""
    return (
        matriz[p1][p2] + matriz[p1][p3]
        + matriz[p2][p1] + matriz[p2][p3]
        + matriz[p3][p1] + matriz[p3][p2]
    )


def cota_resto(matriz, libres):
    """Cota inferior (optimista) del conflicto que aportaran los equipos
    que quedan por formar con los participantes de 'libres'.

    Para cada participante libre i, en el mejor de los casos su conflicto
    saliente hacia el resto del equipo sera al menos el minimo de c[i][x]
    entre los demas libres, y su conflicto entrante sera al menos el
    minimo de c[x][i] entre los demas libres. Sumando esas dos cantidades
    para todos los libres se obtiene una cota que nunca sobreestima el
    coste real restante (ningun equipo puede dar a un participante menos
    conflicto que sus propios minimos), por lo que es valida para B&B:
    nunca podra descartar la solucion optima.
    """
    if len(libres) < 2:
        return 0

    total = 0
    for i in libres:
        min_saliente = min(matriz[i][x] for x in libres if x != i)
        min_entrante = min(matriz[x][i] for x in libres if x != i)
        total += min_saliente + min_entrante
    return total


def resolver_branch_and_bound(matriz):
    """Ramificacion y poda con exploracion en orden de mejor cota (cola de
    prioridad), tal como exige el esquema clasico de B&B.

    Representacion de un nodo: (cota, coste_parcial, equipos_formados, libres)
    - equipos_formados: tupla de ternas ya cerradas
    - libres: tupla de participantes aun sin asignar a ningun equipo
    Un nodo es una solucion completa cuando libres == ().

    Ramificacion: se fija el participante de menor indice en 'libres' (p1)
    y se genera un nodo hijo por cada pareja (p2, p3) posible que lo
    acompane en su equipo. Esto evita generar la misma particion en
    distinto orden (el numero de hojas del arbol es exactamente el numero
    de particiones en equipos de 3, sin repeticiones).

    Poda: al explorar mejor-primero (menor cota primero), en cuanto la
    cota del nodo extraido es >= a la mejor solucion completa encontrada,
    se puede terminar toda la busqueda: ningun nodo pendiente en la cola
    (todos con cota >= la del extraido) puede mejorar esa solucion.
    """
    n = len(matriz)
    todos = tuple(range(n))

    nodos_generados = 1  # contamos la raiz
    cota_raiz = cota_resto(matriz, todos)

    # Cola de prioridad: (cota, coste_parcial, equipos_formados, libres)
    # Se desempata por coste_parcial para que heapq no necesite comparar
    # las tuplas/listas de equipos cuando las cotas coinciden.
    contador_desempate = itertools.count()
    frontera = [(cota_raiz, 0, next(contador_desempate), (), todos)]

    mejor_valor = float("inf")

    while frontera:
        cota, coste_parcial, _, equipos_formados, libres = heapq.heappop(frontera)

        # Poda global: como exploramos en orden creciente de cota, si este
        # nodo ya no puede mejorar la mejor solucion conocida, ninguno de
        # los nodos restantes en la frontera podra hacerlo tampoco.
        if cota >= mejor_valor:
            break

        if not libres:
            # Solucion completa: por construccion, coste_parcial == cota
            mejor_valor = coste_parcial
            continue

        p1 = libres[0]
        resto = libres[1:]

        for i in range(len(resto)):
            for j in range(i + 1, len(resto)):
                p2, p3 = resto[i], resto[j]

                nuevo_coste = coste_parcial + coste_equipo(matriz, p1, p2, p3)
                nuevos_libres = tuple(p for p in resto if p != p2 and p != p3)

                nueva_cota = nuevo_coste + cota_resto(matriz, nuevos_libres)
                nodos_generados += 1

                # Poda local: no encolamos nodos que ya no pueden mejorar
                # la mejor solucion completa encontrada hasta el momento.
                if nueva_cota >= mejor_valor:
                    continue

                nuevos_equipos = equipos_formados + ((p1, p2, p3),)
                heapq.heappush(
                    frontera,
                    (nueva_cota, nuevo_coste, next(contador_desempate),
                     nuevos_equipos, nuevos_libres),
                )

    return mejor_valor, nodos_generados


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
        n = len(matriz)
        if n % 3 != 0:
            print(f"Saltando Caso {idx}: N={n} no es multiplo de 3")
            continue

        inicio = time.perf_counter()
        valor_optimo, nodos = resolver_branch_and_bound(matriz)
        fin = time.perf_counter()

        tiempo_ms = (fin - inicio) * 1000
        resultados.append(
            {
                "problema": idx,
                "n": n,
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
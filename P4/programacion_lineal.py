import pulp
import time
import itertools
import sys

def leer_matrices_entrada(ruta_entrada):
    """Lee una o varias matrices cuadradas en bloques [N + N filas]."""
    try:
        with open(ruta_entrada, "r", encoding="utf-8") as f:
            lineas = [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_entrada}")
        sys.exit(1)

    if not lineas:
        raise ValueError("El fichero de entrada está vacío")

    def leer_bloque(tokens, inicio):
        if inicio >= len(tokens):
            raise ValueError("Falta la dimensión de la matriz")

        n = int(tokens[inicio])
        if n <= 0:
            raise ValueError("La dimensión N debe ser mayor que 0")

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
    idx = 0
    while idx < len(lineas):
        matriz, idx = leer_bloque(lineas, idx)
        matrices.append(matriz)

    return matrices

def resolver_programacion_lineal(matriz_conflictos):
    """Resuelve el problema usando Programación Lineal Entera (Tarea 4)."""
    n = len(matriz_conflictos)
    # 1. Crear el problema de minimización
    prob = pulp.LpProblem("Minimizar_Conflicto_Hackathon", pulp.LpMinimize)

    # 2. Generar todas las combinaciones posibles de 3 personas (ternas) 
    participantes = range(n)
    ternas = list(itertools.combinations(participantes, 3))

    # 3. Definir variables binarias: x_terna = 1 si se elige ese equipo [cite: 82]
    x = pulp.LpVariable.dicts("equipo", ternas, cat=pulp.LpBinary)

    # 4. Función Objetivo: Minimizar nivel total de conflicto [cite: 42, 45]
    costes_ternas = {}
    for terna in ternas:
        i, j, k = terna
        # El nivel de conflicto es la suma de los conflictos de cada miembro hacia los otros dos [cite: 43]
        # Nota: c_ij puede ser distinto de c_ji [cite: 42]
        coste = (matriz_conflictos[i][j] + matriz_conflictos[i][k] +
                 matriz_conflictos[j][i] + matriz_conflictos[j][k] +
                 matriz_conflictos[k][i] + matriz_conflictos[k][j])
        costes_ternas[terna] = coste

    prob += pulp.lpSum([x[terna] * costes_ternas[terna] for terna in ternas])

    # 5. Restricción: Cada participante debe pertenecer exactamente a un equipo 
    for p in participantes:
        prob += pulp.lpSum([x[terna] for terna in ternas if p in terna]) == 1

    # 6. Resolver y medir tiempo
    inicio = time.perf_counter()
    prob.solve(pulp.PULP_CBC_CMD(msg=0)) # Solver por defecto (Tarea 4.2) [cite: 83]
    fin = time.perf_counter()

    tiempo_ms = (fin - inicio) * 1000
    valor_optimo = pulp.value(prob.objective)

    return valor_optimo, tiempo_ms

def main():
    # Validar argumentos de línea de comandos [cite: 51, 53]
    if len(sys.argv) != 3:
        print("Uso: python formarEquiposPL.py <fichero_entrada> <fichero_salida>")
        return

    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2]

    try:
        matrices = leer_matrices_entrada(ruta_entrada)
    except Exception as e:
        print(f"Error al procesar la entrada: {e}")
        return

    resultados_lineas = []
    
    for idx, matriz in enumerate(matrices, 1):
        n = len(matriz)
        # Solo resolvemos si N es múltiplo de 3 
        if n % 3 != 0:
            print(f"Saltando Caso {idx}: N={n} no es múltiplo de 3")
            continue

        valor, tiempo = resolver_programacion_lineal(matriz)
        
        # Formatear salida según requerimientos de la Tarea 2 
        res = (f"Caso {idx}:\n"
               f"  Tiempo de ejecución: {tiempo:.3f} ms\n"
               f"  Valor óptimo (mínimo conflicto): {int(valor)}\n"
               f"{'-'*40}")
        resultados_lineas.append(res)
        print(res)

    # Escribir en el fichero de resultados [cite: 58]
    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write("\n".join(resultados_lineas))
        print(f"\nResultados guardados en: {ruta_salida}")
    except IOError as e:
        print(f"Error al escribir el fichero de salida: {e}")

if __name__ == "__main__":
    main()
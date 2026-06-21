from typing import List, Dict, Set
import sys
import time


# ==============================================================================
# ESTRUCTURA DE DATOS
# Se usa un set (tabla hash) en lugar de una lista para que la búsqueda de
# palabras sea O(1) en lugar de O(n). Esto es esencial para que el coste del
# algoritmo dependa del tamaño del texto y no del diccionario.
# ==============================================================================

def crear_diccionario(path: str) -> Set[str]:
    with open(path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    return set(p.strip() for p in contenido.split(',') if p.strip())


# ==============================================================================
# VARIANTE 1 — Recursión pura (sin memoria)
#
# Para cada posición 'inicio', prueba todos los prefijos posibles.
# Si un prefijo está en el diccionario, llama recursivamente sobre el resto.
# No guarda ningún resultado: si dos ramas distintas llegan al mismo sufijo,
# lo recalcula desde cero. Coste: O(2^n) en el peor caso.
# ==============================================================================

def variante1(diccionario: Set[str], texto: str, inicio: int,
              resultado: List[str], todas: List[List[str]]):
    if inicio == len(texto):
        todas.append(resultado[:])
        return
    for fin in range(inicio + 1, len(texto) + 1):
        sub = texto[inicio:fin]
        if sub in diccionario:
            resultado.append(sub)
            variante1(diccionario, texto, fin, resultado, todas)
            resultado.pop()


# ==============================================================================
# VARIANTE 2 — Recursión con memoización (top-down)
#
# Igual que la variante 1 en estructura, pero guarda en memo[i] TODAS las
# particiones válidas de texto[i:]. Si esa posición ya fue calculada,
# se devuelve el resultado directamente sin volver a explorar nada.
#
# Diferencia clave con variante 1: si dos ramas distintas llegan al mismo
# índice i, la segunda reutiliza memo[i] en O(1) en lugar de recomputar.
#
# Coste: O(n^2) subproblemas distintos, cada uno calculado exactamente una vez.
# ==============================================================================

def variante2(diccionario: Set[str], texto: str, inicio: int,
              memo: Dict[int, List[List[str]]]) -> List[List[str]]:
    if inicio == len(texto):
        return [[]]          # caso base: partición vacía, hemos llegado al fin

    if inicio in memo:
        return memo[inicio]  # ya calculado: devolvemos sin recomputar

    resultado = []
    for fin in range(inicio + 1, len(texto) + 1):
        sub = texto[inicio:fin]
        if sub in diccionario:
            # Obtenemos (memoizadas) todas las particiones del sufijo restante
            for resto in variante2(diccionario, texto, fin, memo):
                resultado.append([sub] + resto)

    memo[inicio] = resultado  # guardamos TODAS las soluciones desde 'inicio'
    return resultado


# ==============================================================================
# VARIANTE 3 — Programación dinámica con tabla (bottom-up)
#
# Sin recursión. Construye tabla[0..n] de izquierda a derecha:
#   tabla[i] = lista de todas las particiones válidas de texto[0:i]
# Para cada j, mira todos los cortes (i,j): si texto[i:j] está en el
# diccionario y tabla[i] no está vacía, extiende cada partición de tabla[i]
# añadiendo texto[i:j] y lo guarda en tabla[j].
# Cada subproblema se calcula exactamente una vez, sin overhead de recursión.
#
# Coste: O(n^2) iteraciones × O(n) por subcadena → O(n^3) pero sin recursión.
# En la práctica es la variante más rápida para textos largos.
# ==============================================================================

def variante3(diccionario: Set[str], texto: str) -> List[List[str]]:
    n = len(texto)
    tabla: List[List[List[str]]] = [[] for _ in range(n + 1)]
    tabla[0] = [[]]  # base: la cadena vacía tiene una única partición (vacía)

    for j in range(1, n + 1):
        for i in range(0, j):
            sub = texto[i:j]
            if sub in diccionario and tabla[i]:
                for particion in tabla[i]:
                    tabla[j].append(particion + [sub])

    return tabla[n]


# ==============================================================================
# MAIN
# ==============================================================================

def main(args):
    if len(args) < 3:
        print("Uso: separarPalabras <variante 1|2|3> <diccionario> <texto>")
        sys.exit(1)

    variante_num = args[0]
    path_dic     = args[1]
    texto        = args[2]

    diccionario = crear_diccionario(path_dic)

    inicio = time.perf_counter()

    if variante_num == "1":
        todas = []
        variante1(diccionario, texto, 0, [], todas)
        soluciones = todas

    elif variante_num == "2":
        memo = {}
        soluciones = variante2(diccionario, texto, 0, memo)

    elif variante_num == "3":
        soluciones = variante3(diccionario, texto)

    else:
        print("Variante no reconocida. Usa 1, 2 o 3.")
        sys.exit(1)

    fin = time.perf_counter()

    if soluciones:
        print(f"Sí. La cadena '{texto}' se puede segmentar como:")
        for sol in soluciones:
            print(" ".join(sol))
    else:
        print(f"No. La cadena '{texto}' no puede segmentarse con el diccionario dado.")

    print(f"\nTiempo de ejecución: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main(sys.argv[1:])
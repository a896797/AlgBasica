from typing import List, Dict, Set
import sys
import time


# ==============================================================================
# ESTRUCTURA DE DATOS
# Se usa un set (tabla hash) en lugar de una lista para que la búsqueda de
# palabras sea O(1) en lugar de O(n). Esto es crucial para que las diferencias
# entre variantes sean apreciables.
# ==============================================================================

def crear_diccionario(path: str) -> Set[str]:
    """Lee el fichero y devuelve un conjunto (set) de palabras."""
    with open(path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    return set(p.strip() for p in contenido.split(',') if p.strip())


# ==============================================================================
# VARIANTE 1 — Recursión pura (sin memoria)
# Recorre todos los prefijos posibles del texto restante. Si un prefijo está
# en el diccionario, explora recursivamente el sufijo. No almacena nada:
# puede recalcular el mismo subproblema muchas veces.
# Coste: exponencial en el peor caso — O(2^n) aproximadamente.
# ==============================================================================

def variante1(diccionario: Set[str], texto: str, inicio: int, resultado: List[str], todas: List[List[str]]):
    """
    Recursión pura. Explora todos los posibles cortes desde la posición 'inicio'.
    - diccionario: conjunto de palabras válidas
    - texto: cadena completa de entrada
    - inicio: posición actual desde donde buscamos el siguiente corte
    - resultado: lista de palabras encontradas hasta ahora (en esta rama)
    - todas: lista acumuladora de todas las soluciones completas encontradas
    """
    if inicio == len(texto):
        # Hemos llegado al final: guardamos esta partición como solución válida
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
# Igual que la variante 1, pero almacena en un diccionario (memo) si desde
# la posición i existe al menos una partición válida. Así, si ya se calculó
# que desde i no hay solución, no se vuelve a explorar.
# Coste: O(n^2) llamadas distintas, cada una O(n) → O(n^3) total.
# La memoización es útil sobre todo cuando hay muchas ramas sin solución.
# ==============================================================================

def variante2_helper(diccionario: Set[str], texto: str, inicio: int,
                     memo: Dict[int, bool]) -> bool:
    """
    Devuelve True si el sufijo texto[inicio:] puede particionarse.
    Usa memo para no repetir cálculos.
    """
    if inicio == len(texto):
        return True
    if inicio in memo:
        return memo[inicio]

    for fin in range(inicio + 1, len(texto) + 1):
        sub = texto[inicio:fin]
        if sub in diccionario and variante2_helper(diccionario, texto, fin, memo):
            memo[inicio] = True
            return True

    memo[inicio] = False
    return False


def variante2(diccionario: Set[str], texto: str, inicio: int,
              resultado: List[str], todas: List[List[str]], memo: Dict[int, bool]):
    """
    Recursión con memoización. Antes de explorar una rama, comprueba si
    desde esa posición existe alguna solución (usando memo). Si no la hay,
    poda la rama y ahorra trabajo.
    """
    if inicio == len(texto):
        todas.append(resultado[:])
        return

    for fin in range(inicio + 1, len(texto) + 1):
        sub = texto[inicio:fin]
        if sub in diccionario:
            # Poda: solo entramos si desde 'fin' existe al menos una solución
            if variante2_helper(diccionario, texto, fin, memo):
                resultado.append(sub)
                variante2(diccionario, texto, fin, resultado, todas, memo)
                resultado.pop()


# ==============================================================================
# VARIANTE 3 — Programación dinámica con tabla (bottom-up)
# Construye la tabla de izquierda a derecha: tabla[i] contiene todas las
# listas de palabras que forman una partición válida de texto[0:i].
# Cada subproblema se calcula UNA SOLA VEZ, en orden, sin recursión.
# Coste: O(n^2) iteraciones × O(n) por comparación de subcadena → O(n^3).
# Pero en la práctica es mucho más rápido que las variantes anteriores porque
# no hay overhead de llamadas recursivas ni riesgo de repetición.
# ==============================================================================

def variante3(diccionario: Set[str], texto: str) -> List[List[str]]:
    """
    Tabla bottom-up. tabla[i] = lista de todas las particiones de texto[0:i].
    Se avanza de izquierda a derecha; para cada posición j, se mira todos los
    cortes (i, j) tales que texto[i:j] esté en el diccionario y tabla[i] no
    esté vacía.
    """
    n = len(texto)
    # tabla[i] almacena todas las particiones válidas de texto[0:i]
    tabla: List[List[List[str]]] = [[] for _ in range(n + 1)]
    tabla[0] = [[]]  # Base: la cadena vacía tiene una única partición: la vacía

    for j in range(1, n + 1):
        for i in range(0, j):
            sub = texto[i:j]
            if sub in diccionario and tabla[i]:
                # Para cada partición que llegaba a i, extendemos con 'sub'
                for particion in tabla[i]:
                    tabla[j].append(particion + [sub])

    return tabla[n]  # Todas las particiones válidas de la cadena completa


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
        todas = []
        # Precalculamos la memo completa de una sola pasada
        variante2_helper(diccionario, texto, 0, memo)
        variante2(diccionario, texto, 0, [], todas, memo)
        soluciones = todas

    elif variante_num == "3":
        soluciones = variante3(diccionario, texto)

    else:
        print("Variante no reconocida. Usa 1, 2 o 3.")
        sys.exit(1)

    fin = time.perf_counter()

    # Mostrar resultados
    if soluciones:
        print(f"Sí. La cadena '{texto}' se puede segmentar como:")
        for sol in soluciones:
            print(" ".join(sol))
    else:
        print(f"No. La cadena '{texto}' no puede segmentarse con el diccionario dado.")

    print(f"\nTiempo de ejecución: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    main(sys.argv[1:])
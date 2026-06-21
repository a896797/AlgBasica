#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import sys
import time


@dataclass
class CasoPrueba:
    n_localidades : int
    n_carreteras  : int
    n_centros_act : int
    centros_act   : List[int]
    centros_nuevos: int
    matriz        : np.ndarray


def floyd_warshall(mat: np.ndarray) -> None:
    n = mat.shape[0]
    for k in range(n):
        np.minimum(mat, mat[:, k : k + 1] + mat[k : k + 1, :], out=mat)


def peor_tiempo(mat: np.ndarray, centros: List[int]) -> float:
    if not centros:
        return float("inf")
    # sacamos el mínimo por filas (centro más cercano) y luego el máximo global
    return float(np.max(np.min(mat[:, centros], axis=1)))


def precomputar_min_right(mat: np.ndarray, n: int, excluidos: set) -> np.ndarray:
    # Precalculo para la cota P2, distancias mínimas acumuladas de derecha a izquierda
    mr = np.full((n, n + 1), np.inf)
    for s in range(n - 1, -1, -1):
        if s not in excluidos:
            np.minimum(mat[:, s], mr[:, s + 1], out=mr[:, s])
        else:
            mr[:, s] = mr[:, s + 1]
    return mr


def cota_inferior(dist_act: np.ndarray, ultimo_j: int, min_right: np.ndarray) -> float:
    # Calcula el peor tiempo hipotético si pusieramos centros infinitos a partir de ultimo_j
    return float(np.max(np.minimum(dist_act, min_right[:, ultimo_j + 1])))


def bt_sin_poda(mat: np.ndarray, n: int, centros: List[int], excluidos: set,
                k_rest: int, inicio: int, dist_act: np.ndarray, mejor: List) -> None:
    mejor[2] += 1  # Contador de nodos generados
    
    # base, todos los centros colocados
    if k_rest == 0:
        t = float(np.max(dist_act))
        if t < mejor[0]:
            mejor[0], mejor[1] = t, [c for c in centros if c not in excluidos]
        return

    # Exploración combinatoria pura (siguiendo orden creciente para evitar permutaciones)
    for j in range(inicio, n):
        if j not in excluidos:
            nueva_dist = np.minimum(dist_act, mat[:, j])
            centros.append(j)
            bt_sin_poda(mat, n, centros, excluidos, k_rest - 1, j + 1, nueva_dist, mejor)
            centros.pop()  # Backtracking


def bt_con_poda(mat: np.ndarray, n: int, centros: List[int], excluidos: set,
                k_rest: int, inicio: int, dist_act: np.ndarray, mejor: List, min_right: np.ndarray) -> None:
    mejor[2] += 1
    
    if k_rest == 0:
        t = float(np.max(dist_act))
        if t < mejor[0]:
            mejor[0], mejor[1] = t, [c for c in centros if c not in excluidos]
        return

    # Poda P1, si no quedan suficientes pueblos en el bucle para rellenar K, abortamos
    if n - inicio < k_rest:
        return

    # Heurística, evaluamos y ordenamos candidatos por su peor-tiempo parcial
    candidatos = []
    for j in range(inicio, n):
        if j not in excluidos:
            d_j = np.minimum(dist_act, mat[:, j])
            candidatos.append((float(np.max(d_j)), j, d_j))

    candidatos.sort(key=lambda x: x[0])  # El que mejor pinte primero para actualizar mejor_global rápido

    # Bucle de exploración con poda P2
    for t_j, j, d_j in candidatos:
        # Poda P2, si la cota es peor que nuestro mejor actual, podamos
        if cota_inferior(d_j, j, min_right) >= mejor[0]:
            continue
            
        centros.append(j)
        bt_con_poda(mat, n, centros, excluidos, k_rest - 1, j + 1, d_j, mejor, min_right)
        centros.pop()


def leer_casos(path: str) -> List[CasoPrueba]:
    try:
        with open(path, encoding="utf-8") as f:
            tokens = f.read().split()
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichero de entrada no encontrado: '{path}'")

    pos = 0
    def leer_int(contexto: str = "") -> int:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError(f"Fin de fichero inesperado. {contexto}")
        try:
            val = int(tokens[pos]); pos += 1; return val
        except ValueError:
            raise ValueError(f"Se esperaba entero, se obtuvo '{tokens[pos-1]}'. {contexto}")

    num_casos = leer_int("número de casos de prueba")
    if num_casos <= 0:
        raise ValueError("El número de casos debe ser positivo.")

    casos = []
    for nc in range(1, num_casos + 1):
        ctx = f"[Caso {nc}]"
        n, m, c, k = leer_int(f"{ctx} n"), leer_int(f"{ctx} m"), leer_int(f"{ctx} c"), leer_int(f"{ctx} k")

        if n <= 0 or any(x < 0 for x in (m, c, k)) or c + k > n:
            raise ValueError(f"{ctx} Parámetros inválidos o incompatibles.")

        # Matriz de adyacencia inicial
        mat = np.full((n, n), np.inf)
        np.fill_diagonal(mat, 0.0)

        for _ in range(m):
            v, w, t = leer_int(f"{ctx} v") - 1, leer_int(f"{ctx} w") - 1, leer_int(f"{ctx} t")
            if not (0 <= v < n and 0 <= w < n) or t < 0:
                raise ValueError(f"{ctx} Restricciones de arista violadas.")
            # Control de carreteras duplicadas (nos quedamos con la más rápida)
            mat[v, w] = mat[w, v] = min(mat[v, w], t)

        centros_act = [leer_int(f"{ctx} centro") - 1 for _ in range(c)]
        if any(not (0 <= ce < n) for ce in centros_act) or len(set(centros_act)) != c:
            raise ValueError(f"{ctx} Centros existentes erróneos o duplicados.")

        # Dejamos la matriz lista con los caminos mínimos reales
        floyd_warshall(mat)
        casos.append(CasoPrueba(n, m, c, centros_act, k, mat))
        
    return casos


def resolver(caso: CasoPrueba, usar_poda: bool) -> Tuple[float, int, float, List[int]]:
    n = caso.n_localidades
    excluidos = set(caso.centros_act)
    centros = list(caso.centros_act)
    
    # Calculamos el estado de distancias inicial solo con lo que ya está construido
    dist_ini = np.min(caso.matriz[:, centros], axis=1).astype(float) if centros else np.full(n, np.inf)
    mejor = [float("inf"), [], 0]

    t0 = time.perf_counter()
    if usar_poda:
        min_right = precomputar_min_right(caso.matriz, n, excluidos)
        bt_con_poda(caso.matriz, n, centros, excluidos, caso.centros_nuevos, 0, dist_ini, mejor, min_right)
    else:
        bt_sin_poda(caso.matriz, n, centros, excluidos, caso.centros_nuevos, 0, dist_ini, mejor)
    
    tiempo_ms = (time.perf_counter() - t0) * 1000.0
    return tiempo_ms, mejor[2], mejor[0], sorted(c + 1 for c in mejor[1])


def escribir_resultados(resultados: List[Tuple[float, int, float, List[int]]], path: str) -> None:
    lineas = []
    for tiempo_ms, n_nodos, val_opt, centros_nuevos in resultados:
        # Formateo del valor óptimo para evitar decimales si da entero clavado
        val_str = "inf" if np.isinf(val_opt) else (str(int(val_opt)) if val_opt == int(val_opt) else f"{val_opt:.1f}")
        centros_str = " ".join(map(str, centros_nuevos))
        linea = f"{tiempo_ms:.2f} {n_nodos} {val_str} {centros_str}".strip()
        lineas.append(linea)
        print(linea)
        
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")


def main(args: List[str]) -> None:
    if len(args) < 2:
        print("Uso: python ubicaCentros.py <entrada> <salida> [0=sin_poda | 1=con_poda]")
        sys.exit(1)

    usar_poda = (int(args[2]) != 0) if len(args) > 2 else True
    try:
        casos = leer_casos(args[0])
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR en la entrada: {exc}", file=sys.stderr)
        sys.exit(1)

    resultados = [resolver(c, usar_poda) for c in casos]
    escribir_resultados(resultados, args[1])


if __name__ == "__main__":
    main(sys.argv[1:])
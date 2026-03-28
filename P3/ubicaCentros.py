from typing import List
import numpy as np
import sys
from dataclasses import dataclass

# Estructura para almacenar los datos de cada escenario de prueba
@dataclass
class Caso_prueba:
    centros_act: List[int]
    n_centros_act: int
    centros_nuevos: int
    centros_nuevos_puestos: List[int]
    n_localidades: int
    n_carreteras: int
    matriz: np.ndarray

def leer_casos(path, casos):
    """
    Carga los datos desde el archivo de texto. 
    Ajusta los índices de las localidades para trabajar con la matriz.
    """
    with open(path, 'r') as f:
        lineas = f.readlines()
    
    idx = 0
    num_casos = int(lineas[idx].strip())
    idx += 1
    
    for _ in range(num_casos):
        datos = list(map(int, lineas[idx].strip().split()))
        n, m, c, k = datos[0], datos[1], datos[2], datos[3]
        idx += 1
        
        # Inicializamos matriz con infinito
        matriz = np.full((n, n), np.inf, dtype=float)
        np.fill_diagonal(matriz, 0) 
        
        for i in range(m):
            v, w, t = map(int, lineas[idx].strip().split())
            v -= 1
            w -= 1
            matriz[v][w] = t
            matriz[w][v] = t 
            idx += 1
        
        centros_existentes = list(map(int, lineas[idx].strip().split()))
        centros_existentes = [c - 1 for c in centros_existentes]
        idx += 1
        
        caso = Caso_prueba(
            n_localidades=n,
            n_carreteras=m,
            n_centros_act=c,
            centros_act=centros_existentes,
            centros_nuevos=k,
            centros_nuevos_puestos=[],
            matriz=matriz
        )
        casos.append(caso)
    
    return casos

def calcular_distancias(caso):
    """
    Calcula la calidad de la solución actual.
    Para cada localidad, busca la distancia al centro más cercano.
    """
    n = caso.n_localidades
    dist_total = 0
    
    for i in range(n):
        if i in caso.centros_act:
            continue

        min_dist = np.inf
        for j in range(n):
            if j in caso.centros_act:
                min_dist = min(min_dist, caso.matriz[i][j])
        
        dist_total += min_dist
    
    return dist_total, 1

def seleccion_centros(caso, centros_faltantes, centros_actuales=None, centros_iniciales=None):
    """
    Algoritmo de Backtracking estándar sin optimizaciones.
    Explora todas las combinaciones posibles de nuevos centros.
    """
    if centros_actuales is None:
        centros_actuales = caso.centros_act.copy()
        centros_iniciales = centros_actuales.copy()
    
    # Caso base: hemos colocado todos los centros requeridos
    if centros_faltantes == 0:
        dist, _ = calcular_distancias(caso)
        centros_nuevos = [c for c in centros_actuales if c not in centros_iniciales]
        return dist, 1, centros_nuevos
    
    mejor_distancia = np.inf
    total_nodos = 1
    mejores_centros = []
    
    # Probamos a poner un centro en cada localidad disponible
    for j in range(caso.n_localidades):
        if j not in centros_actuales:
            centros_actuales.append(j)
            caso.centros_act = centros_actuales
            
            distancia, n_nodos, centros_nuevos = seleccion_centros(caso, centros_faltantes - 1, centros_actuales, centros_iniciales)
            
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejores_centros = centros_nuevos
            total_nodos += n_nodos
            
            # Retroceso, quitamos el centro añadido para probar la siguiente opción
            centros_actuales.pop()
    
    return mejor_distancia, total_nodos, mejores_centros

def seleccion_centros_con_poda(caso, centros_faltantes, centros_actuales=None, centros_iniciales=None, mejor_global=None):
    """
    Versión optimizada con Poda por Cota Optimista.
    Usa el mejor resultado encontrado hasta el momento para descartar ramas inútiles.
    """
    if centros_actuales is None:
        centros_actuales = caso.centros_act.copy()
        centros_iniciales = centros_actuales.copy()
        mejor_global = [np.inf] # Usamos lista para paso por referencia
    
    if centros_faltantes == 0:
        dist, _ = calcular_distancias(caso)
        centros_nuevos = [c for c in centros_actuales if c not in centros_iniciales]
        if dist < mejor_global[0]:
            mejor_global[0] = dist
        return dist, 1, centros_nuevos
    
    # Evaluamos el impacto de cada opción antes de profundizar
    opciones = []
    for j in range(caso.n_localidades):
        if j not in centros_actuales:
            centros_temp = centros_actuales + [j]
            caso.centros_act = centros_temp
            dist_parcial, _ = calcular_distancias(caso)
            opciones.append((dist_parcial, j))
    
    # Ordenamos opciones de mejor a peor para encontrar el óptimo antes
    opciones.sort()
    
    mejor_distancia = np.inf
    total_nodos = 1
    mejores_centros = []
    
    for dist_parcial, j in opciones:
        # PODA: Si el estado actual ya es peor que el mejor global, no seguimos
        if dist_parcial >= mejor_global[0]:
            break  
        
        centros_actuales.append(j)
        caso.centros_act = centros_actuales
        
        distancia, n_nodos, centros_nuevos = seleccion_centros_con_poda(caso, centros_faltantes - 1, centros_actuales, centros_iniciales, mejor_global)
        
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejores_centros = centros_nuevos
        total_nodos += n_nodos
        
        centros_actuales.pop()
    
    # Si la rama fue podada totalmente, devolvemos el mejor global
    if mejor_distancia == np.inf:
        return mejor_global[0], total_nodos, []
    
    return mejor_distancia, total_nodos, mejores_centros

def mostrar_resultados(resultados, output_path=None):

    lineas_salida = []
    
    for tiempo_ms, n_nodos, valor_optimo, caso in resultados:
        centros_ordenados = sorted([c + 1 for c in caso.centros_nuevos_puestos])
        
        # Formato: tiempo nodos valor s1 s2 ... sk
        linea = f"{tiempo_ms:.2f} {n_nodos} {valor_optimo}"
        for centro in centros_ordenados:
            linea += f" {centro}"
        
        lineas_salida.append(linea)
        print(linea)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write('\n'.join(lineas_salida))

def main(args): 
    import time
    
    if len(args) < 3:
        print("Uso: python ubicaCentros.py <entrada> <salida> <0|1>")
        sys.exit(1)
    
    fichero_entrada = args[0]
    fichero_salida = args[1]
    formato = int(args[2]) # 0 = sin poda, 1 = con poda
    
    casos = []
    leer_casos(fichero_entrada, casos)
    
    resultados = []
    for caso in casos:
        inicio = time.time()
        
        if formato == 0:
            valor_optimo, n_nodos, centros_nue = seleccion_centros(caso, caso.centros_nuevos)
        else:
            valor_optimo, n_nodos, centros_nue = seleccion_centros_con_poda(caso, caso.centros_nuevos)
        
        fin = time.time()
        tiempo_ms = (fin - inicio) * 1000
        
        caso.centros_nuevos_puestos = centros_nue
        resultados.append((tiempo_ms, n_nodos, valor_optimo, caso))
    
    mostrar_resultados(resultados, fichero_salida)

if __name__ == "__main__":  
    main(sys.argv[1:])
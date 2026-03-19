from ast import List
import numpy as np
import sys
from dataclasses import dataclass

n_casos = 0
@dataclass
class Caso_prueba:
    centros_act: List[int]
    n_centros_act: int
    centros_nuevos: int
    centros_nuevos_puestos: List[int]
    n_localidades: int
    n_carreteras: int
    matriz: np.ndarray
    

def leer_casos (path, casos) :
    """
    Lee los casos de prueba del fichero especificado.
    
    Formato del fichero:
    - Primera línea: número total de casos
    - Para cada caso:
        - Línea: n, m, c, k (vértices, aristas, centros actuales, nuevos centros)
        - Siguientes m líneas: v, w, t (carreteras)
        - Última línea: c números (localidades con centros existentes)
    """
    with open(path, 'r') as f:
        lineas = f.readlines()
    
    idx = 0
    num_casos = int(lineas[idx].strip())
    idx += 1
    
    for _ in range(num_casos):
        # Leer n, m, c, k
        datos = list(map(int, lineas[idx].strip().split()))
        n, m, c, k = datos[0], datos[1], datos[2], datos[3]
        idx += 1
        
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
    n = caso.n_localidades
    dist = 0
    
    for i in range(n):
        if i in caso.centros_act:
            continue

        min_dist = np.inf
        for j in range(n):
            if j in caso.centros_act:
                min_dist = min(min_dist, caso.matriz[i][j])
        
        dist += min_dist
    
    return dist, 1


def seleccion_centros(caso, centros_faltantes, centros_actuales=None):
    if centros_actuales is None:
        centros_actuales = caso.centros_act.copy()
    
    if centros_faltantes == 0:
        return calcular_distancias(caso)
    
    mejor_distancia = np.inf
    total_nodos = 1
    
    for j in range(caso.n_localidades):
        if j not in centros_actuales:
            centros_actuales.append(j)
            caso.centros_act = centros_actuales
            
            distancia, n_nodos = seleccion_centros(caso, centros_faltantes - 1, centros_actuales)
            mejor_distancia = min(mejor_distancia, distancia)
            total_nodos += n_nodos
            
            centros_actuales.pop()
    
    return mejor_distancia, total_nodos


def seleccion_centros_con_poda(caso, centros_faltantes, centros_actuales=None, mejor_dist_global=None, contador_nodos=None):

    if centros_actuales is None:
        centros_actuales = caso.centros_act.copy()
        mejor_dist_global = [np.inf]  # Mejor distancia encontrada hasta ahora
        contador_nodos = [0]  # Total de nodos explorados
    
    contador_nodos[0] += 1  # Contar este nodo
    
    if centros_faltantes == 0:
        dist_actual, _ = calcular_distancias(caso)
        if dist_actual < mejor_dist_global[0]:
            mejor_dist_global[0] = dist_actual
        return dist_actual, 1
    
    mejor_distancia = np.inf
    total_nodos = 1
    
    for j in range(caso.n_localidades):
        if j not in centros_actuales:
            centros_actuales.append(j)
            caso.centros_act = centros_actuales
            
            dist_actual, _ = calcular_distancias(caso)
            
            # Poda: solo explorar si esta rama puede mejorar la mejor solución
            if dist_actual < mejor_dist_global[0]:
                distancia, n_nodos = seleccion_centros_con_poda(
                    caso, 
                    centros_faltantes - 1, 
                    centros_actuales,
                    mejor_dist_global,
                    contador_nodos
                )
                mejor_distancia = min(mejor_distancia, distancia)
                total_nodos += n_nodos
            
            centros_actuales.pop()
    
    return mejor_distancia, total_nodos



def mostrar_resultados(resultados, output_path=None):
    lineas_salida = []
    
    for tiempo_ms, n_nodos, valor_optimo, caso in resultados:
        centros_ordenados = sorted([c + 1 for c in caso.centros_nuevos_puestos])
        
        linea = f"{tiempo_ms} {n_nodos} {valor_optimo}"
        
        for centro in centros_ordenados:
            linea += f" {centro}"
        
        lineas_salida.append(linea)
        print(linea)
    
    if output_path:
        try:
            with open(output_path, 'w') as f:
                f.write('\n'.join(lineas_salida))
            print(f"\nResultados guardados en {output_path}")
        except IOError as e:
            print(f"Error al guardar el fichero de salida: {e}")



def main(args): 
    import time
    
    # Validar argumentos
    if len(args) < 3:
        print("Uso: ubicaCentros <fichero_entrada> <fichero_salida> <formato>")
        print("  formato: 0 = sin poda, 1 = con poda")
        sys.exit(1)
    
    fichero_entrada = args[0]
    fichero_salida = args[1]
    formato = int(args[2])
    
    if formato not in [0, 1]:
        print("Error: formato debe ser 0 (sin poda) o 1 (con poda)")
        sys.exit(1)
    
    casos = List[Caso_prueba]()
    leer_casos(fichero_entrada, casos)
    
    resultados = []
    
    for caso in casos:
        inicio = time.time()
        
        if formato == 0:
            valor_optimo, n_nodos = seleccion_centros(caso, caso.centros_nuevos)
        else:
            valor_optimo, n_nodos = seleccion_centros_con_poda(caso, caso.centros_nuevos)
        
        fin = time.time()
        tiempo_ms = int((fin - inicio) * 1000)
        
        centros_iniciales = caso.centros_act[:caso.n_centros_act]
        caso.centros_nuevos_puestos = [c for c in caso.centros_act if c not in centros_iniciales]
        
        resultados.append((tiempo_ms, n_nodos, valor_optimo, caso))
    
    mostrar_resultados(resultados, fichero_salida)



if __name__ == "__main__":  
    main(sys.argv[1:])



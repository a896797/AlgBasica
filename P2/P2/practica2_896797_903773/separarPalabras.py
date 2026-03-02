from dataclasses import dataclass
from typing import List
import sys
import time

@dataclass
class Diccionario:
    tamano: int
    palabras: List[str]
    
memoria = {}   

def crear_diccionario (path, diccionario) :
    with open (path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    palabras = contenido.split(',') 
    for palabra in palabras:
        # Inicializamos con un tamaño fijo en el main, 10000
        diccionario.palabras[diccionario.tamano] = palabra.strip()
        diccionario.tamano += 1

def variante1(diccionario, palabra_ini, texto, acum, resultado):
    # Fuerza bruta, probamos todas las ramas posibles
    if acum in diccionario.palabras and acum != '':
        if texto[0:1] != '':
            resultado1 = resultado.copy()
            variante1(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado1)
        resultado.append(acum)
        variante1(diccionario, palabra_ini, texto[1:], texto[0:1], resultado)

    elif len(texto) > 0:
        variante1(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado)
    else:
        # Comprobar si la combinación de piezas reconstruye el texto original
        res =""
        for palabra in resultado:
            res +=palabra
            
        if res == palabra_ini:
            for palabra in resultado:
                print(palabra, end=" ")
            print("\n")
        return

def variante2(diccionario, palabra_ini, texto, acum, resultado):
    # Metemos un diccionario global para no repetir cálculos que ya sabemos que fallan o aciertan
    if acum not in memoria:
        if acum in diccionario.palabras and acum != '':
            memoria[acum] = 1 
            if texto[0:1] != '':
                resultado1 = resultado.copy()
                variante2(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado1)
            resultado.append(acum)
            variante2(diccionario, palabra_ini, texto[1:], texto[0:1], resultado)
        elif len(texto) > 0:
            memoria[acum] = 0
            variante2(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado)
        else:
            res =""
            for palabra in resultado:
                res +=palabra
                
            if res == palabra_ini:
                for palabra in resultado:
                    print(palabra, end=" ")
                print("\n")
            return
    elif memoria[acum] == 1:
        if acum != '':
            resultado.append(acum)
            variante2(diccionario, palabra_ini, texto[1:], texto[0:1], resultado)
        else:
            res =""
            for palabra in resultado:
                res +=palabra
            
            if res == palabra_ini:
                for palabra in resultado:
                    print(palabra, end=" ")
                print("\n")
            return
    else:
        if acum != '':
            variante2(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado)
        else:
            res =""
            for palabra in resultado:
                res +=palabra
            
            if res == palabra_ini:
                for palabra in resultado:
                    print(palabra, end=" ")
                print("\n")
            return

def variante3(diccionario, texto, i, tabla, resultado):
    # Enfoque de abajo a arriba (bottom-up) guardando subproblemas en la tabla
    if i == len(texto):
        print(' '.join(resultado))
        return [[]] 

    if i in tabla:
        return tabla[i]

    soluciones_desde_i = []

    for j in range(i + 1, len(texto) + 1):
        sub = texto[i:j]
        if sub in diccionario.palabras:
            # Recursión sobre el resto de la cadena desde el índice j
            for sub_sol in variante3(diccionario, texto, j, tabla, resultado + [sub]):
                soluciones_desde_i.append([sub] + sub_sol)

    tabla[i] = soluciones_desde_i
    return soluciones_desde_i

def main(args):
    # Ajustamos el tamaño a 10000
    diccionario = Diccionario(0, [""]*10000)
    crear_diccionario(args[1], diccionario)
    palabra_ini = args[2]
    resultado = []
    
    # Usamos perf_counter para tener más precisión en las pruebas
    inicio = time.perf_counter()
    
    if (args[0] == "1"):
        variante1(diccionario, palabra_ini, palabra_ini , "", resultado)
    elif (args[0] == "2"):
        variante2(diccionario, palabra_ini, palabra_ini , "", resultado)
    else:
        # Inicializamos tabla para la variante de tabulación
        tabla = {}
        variante3(diccionario, palabra_ini, 0, tabla, resultado)
    
    fin = time.perf_counter()
    
    print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")

if __name__ == "__main__":  
    sys.setrecursionlimit(5000)
    main(sys.argv[1:])
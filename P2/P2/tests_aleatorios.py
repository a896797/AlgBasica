import sys
import time
import random
import string
from dataclasses import dataclass
from typing import List

from separarPalabras import Diccionario, crear_diccionario, variante1, variante2, variante3
import separarPalabras 

def generar_frase_aleatoria(diccionario, num_palabras):
    # Cogemos palabras al azar del dicc para montar la frase
    palabras_validas = [p for p in diccionario.palabras if p != ""]
    if not palabras_validas: return ""
    seleccionadas = random.sample(palabras_validas, min(num_palabras, len(palabras_validas)))
    return "".join(seleccionadas)

def modificar_frase(frase, probabilidad):
    # Metemos ruido cambiando letras segun la prob
    lista_frase = list(frase)
    cambios = 0
    for i in range(len(lista_frase)):
        if random.random() < probabilidad:
            nueva_letra = random.choice(string.ascii_lowercase)
            if lista_frase[i] != nueva_letra:
                lista_frase[i] = nueva_letra
                cambios += 1
    return "".join(lista_frase), cambios

def ejecutar_test(v_num, dic, frase):
    # Resetear la memoria para que los tiempos sean reales cada vez
    separarPalabras.memoria = {} 
    
    inicio = time.perf_counter()
    if v_num == 1:
        variante1(dic, frase, frase, "", [])
    elif v_num == 2:
        variante2(dic, frase, frase, "", [])
    elif v_num == 3:
        variante3(dic, frase, 0, {}, [])
    return time.perf_counter() - inicio

def main():
    # El script espera recibir la variante y la ruta del diccionario
    if len(sys.argv) < 3:
        print("Faltan argumentos (variante o diccionario)")
        return

    variante_elegida = int(sys.argv[1])
    path_dic = sys.argv[2]

    # Cargamos datos (max 10000 palabras)
    dic = Diccionario(0, [""] * 10000)
    crear_diccionario(path_dic, dic)
    
    # 10% del tamaño para la frase aleatoria
    num_pal = dic.tamano
    n_seleccion = max(1, num_pal // 10)
    
    frase_original = generar_frase_aleatoria(dic, n_seleccion)
    if not frase_original:
        print("Error: El diccionario no tiene palabras")
        return

    lf = len(frase_original)
    prob = 1 / (lf * 10)
    frase_ruido, n_cambios = modificar_frase(frase_original, prob)

    print(f"Diccionario: {path_dic} ({num_pal} palabras)")
    print(f"Frase generada (Longitud {lf}): {frase_original}")
    print(f"Probabilidad de ruido (Tarea 3): {prob:.8f} (Letras cambiadas: {n_cambios})")
    print("-" * 50)

    # Si se pasa 0, lanzamos las tres variantes seguidas para comparar
    v_a_ejecutar = [1, 2, 3] if variante_elegida == 0 else [variante_elegida]

    for v in v_a_ejecutar:
        print(f"\nPROBANDO VARIANTE {v}:")
        
        # Escenario 1: Frase limpia
        t1 = ejecutar_test(v, dic, frase_original)
        print(f"  Escenario 1 (Sin modificar): {t1:.6f} seg")
        
        # Escenario 2: Frase con ruido
        t2 = ejecutar_test(v, dic, frase_ruido)
        print(f"  Escenario 2 (Con ruido):    {t2:.6f} seg")

if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    main()
import sys
import time
import random
import string
from dataclasses import dataclass
from typing import List

# Importamos desde tu archivo original
from separarPalabras import Diccionario, crear_diccionario, variante1, variante2, variante3
import separarPalabras # Para limpiar la memoria global

def generar_frase_aleatoria(diccionario, num_palabras):
    palabras_validas = [p for p in diccionario.palabras if p != ""]
    if not palabras_validas: return ""
    seleccionadas = random.sample(palabras_validas, min(num_palabras, len(palabras_validas)))
    return "".join(seleccionadas)

def modificar_frase(frase, probabilidad):
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
    # Limpiamos la memoria antes de cada ejecución para que el tiempo sea real
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
    # El BAT envía: python tests_aleatorios.py "VARIANTE" "DICCIONARIO"
    # sys.argv[0] es el nombre del script
    # sys.argv[1] es la VARIANTE (el "1" que te daba error)
    # sys.argv[2] es el DICCIONARIO
    
    if len(sys.argv) < 3:
        print("Error de argumentos internos.")
        return

    variante_elegida = int(sys.argv[1])
    path_dic = sys.argv[2]

    # Cargamos el diccionario
    dic = Diccionario(0, [""] * 10000)
    crear_diccionario(path_dic, dic)
    
    num_pal = dic.tamano
    n_seleccion = max(1, num_pal // 10)
    
    frase_original = generar_frase_aleatoria(dic, n_seleccion)
    if not frase_original:
        print("Error: El diccionario está vacío.")
        return

    lf = len(frase_original)
    prob = 1 / (lf * 10)
    frase_ruido, n_cambios = modificar_frase(frase_original, prob)

    print(f"Diccionario: {path_dic} ({num_pal} palabras)")
    print(f"Frase generada (LF {lf}): {frase_original}")
    print(f"Probabilidad de ruido: {prob:.8f} (Cambios: {n_cambios})")
    print("-" * 50)

    # Si pones variante 0 en el .bat, probamos las 3. Si pones 1, solo la 1.
    v_a_ejecutar = [1, 2, 3] if variante_elegida == 0 else [variante_elegida]

    for v in v_a_ejecutar:
        print(f"\nPROBANDO VARIANTE {v}:")
        
        t1 = ejecutar_test(v, dic, frase_original)
        print(f"  Escenario 1 (Sin modificar): {t1:.6f} seg")
        
        t2 = ejecutar_test(v, dic, frase_ruido)
        print(f"  Escenario 2 (Con ruido):    {t2:.6f} seg")

if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    main()
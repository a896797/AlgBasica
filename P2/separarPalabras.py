
from dataclasses import dataclass
from typing import List
import sys


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
        diccionario.palabras[diccionario.tamano] = palabra.strip()
        diccionario.tamano += 1

def variante1(diccionario, palabra_ini, texto, acum, resultado):
    if acum in diccionario.palabras and acum != '':
        if texto[0:1] != '':
            resultado1 = resultado.copy()
            variante1(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado1)
        resultado.append(acum)
        print(resultado, "Resultado")
        variante1(diccionario, palabra_ini, texto[1:], texto[0:1], resultado)

    elif len(texto) > 0:
        variante1(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado)
    else:
        res =""
        for palabra in resultado:
            res +=palabra
            
        if res == palabra_ini:
            for palabra in resultado:
                print(palabra, end=" ")
            print("\n")
        return
def variante2(diccionario, palabra_ini, texto, acum, resultado):
    if acum not in memoria:
        if acum in diccionario.palabras and acum != '':
            memoria[acum] = 1 
            if texto[0:1] != '':
                resultado1 = resultado.copy()
                variante2(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado1)
            resultado.append(acum)
            print(resultado, "Resultado")
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
    if i == len(texto):
        print(' '.join(resultado))
        return [[]] 

    if i in tabla:
        return tabla[i]

    soluciones_desde_i = []

    for j in range(i + 1, len(texto) + 1):
        sub = texto[i:j]
        if sub in diccionario.palabras:
            for sub_sol in variante3(diccionario, texto, j, tabla, resultado + [sub]):
                soluciones_desde_i.append([sub] + sub_sol)

    tabla[i] = soluciones_desde_i
    return soluciones_desde_i

def main(args):
    diccionario = Diccionario(0, [""]*1000)
    crear_diccionario(args[1], diccionario)
    palabra_ini = args[2]
    resultado = []
    if (args[0] == "1"):
        variante1(diccionario, palabra_ini, palabra_ini , "", resultado)
    elif (args[0] == "2"):
        variante2(diccionario, palabra_ini, palabra_ini , "", resultado)
    else:
        tabla = {}
        variante3(diccionario, palabra_ini, 0, tabla, resultado)
if __name__ == "__main__":  
    main(sys.argv[1:])


    
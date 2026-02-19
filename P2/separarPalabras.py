
from dataclasses import dataclass
from typing import List
import sys


@dataclass
class Diccionario:
    tamano: int
    palabras: List[str]
    
def crear_diccionario (path, diccionario) :
    with open (path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    palabras = contenido.split(',') 
    for palabra in palabras:
        diccionario.palabras[diccionario.tamano] = palabra.strip()
        diccionario.tamano += 1

def variante1(diccionario, palabra_ini, texto, acum, resultado):
    if acum in diccionario.palabras and acum != ''and :

        print(texto + "Texto")
        print(acum + "Acum")
        resultado1 = resultado.copy()
        variante1(diccionario, palabra_ini, texto[1:], acum + texto[0:1], resultado1)
        resultado.append(acum)
        print(resultado, "Resultado")
        variante1(diccionario, palabra_ini, texto[1:], texto[0:1], resultado)
    elif len(texto) > 0:
        print(texto + "Texto")
        print(acum + "Acum")
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
    
def main(args):
    diccionario = Diccionario(0, [""]*1000)
    crear_diccionario(args[1], diccionario)
    palabra_ini = args[2]
    resultado = []
    variante1(diccionario, palabra_ini, palabra_ini , "", resultado)
    
if __name__ == "__main__":  
    main(sys.argv[1:])


    
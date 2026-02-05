from PIL import Image
from dataclasses import dataclass
from typing import List
import numpy as np
import random
import sys
import time
MARCO = 256

@dataclass
class Clavo:
    x: int
    y: int
    
@dataclass
class Marco_Clavos:
    clavos_arriba: List[Clavo]
    clavos_abajo: List[Clavo]
    clavos_izquierda: List[Clavo]
    clavos_derecha: List[Clavo]
    
@dataclass
class Linea:
    clavo_inicio: Clavo
    clavo_fin: Clavo
    nivel_gris: int
    
@dataclass
class Resultado:
    lineas: List[Linea]
    
def converter_to_matrix(imagen):
    img = Image.open(imagen).convert('L')
    # Estira o reduce la imagen a MARCO x MARCO exactamente
    img = img.resize((MARCO, MARCO), Image.Resampling.LANCZOS)
    img_matrix = np.array(img)
    return img_matrix
    
def posicionar_clavos(Nclavos):
    resto4 = Nclavos % 4
    # Reparto base
    base = Nclavos // 4
    clavos_arriba = base
    clavos_abajo = base
    clavos_izquierda = base
    clavos_derecha = base
    # Repartir el resto
    if resto4 == 1:
        clavos_arriba += 1
    elif resto4 == 2:
        clavos_arriba += 1
        clavos_abajo += 1
    elif resto4 == 3:
        clavos_arriba += 1
        clavos_abajo += 1
        clavos_izquierda += 1

    # Posicionar los clavos en el marco
    clavos_arriba = [Clavo(x=int(i*(MARCO/(clavos_arriba+1))), y=0)
                    for i in range(1, clavos_arriba+1)]

    clavos_abajo = [Clavo(x=int(i*(MARCO/(clavos_abajo+1))), y=MARCO-1)
                    for i in range(1, clavos_abajo+1)]

    clavos_izquierda = [Clavo(x=0, y=int(i*(MARCO/(clavos_izquierda+1))))
                        for i in range(1, clavos_izquierda+1)]

    clavos_derecha = [Clavo(x=int(MARCO-1), y=int(i*(MARCO/(clavos_derecha+1))))
                    for i in range(1, clavos_derecha+1)]

    return Marco_Clavos(clavos_arriba, clavos_abajo, clavos_izquierda, clavos_derecha)

def nivel_gris_bresenham(clavo1, clavo2, imagen):
    x1, y1 = clavo1.x, clavo1.y
    x2, y2 = clavo2.x, clavo2.y
    suma_gris = 0.0
    total_pixeles = 0.0
    # 0 - Distancias
    dy = y2 - y1
    dx = x2 - x1
    
    # 1 - Incrementos para secciones con avance inclinado
    inc_yi = 1 if dy >= 0 else -1
    dy = abs(dy)
    
    inc_xi = 1 if dx >= 0 else -1
    dx = abs(dx)
    
    # 2 - Incrementos para secciones con avance recto
    if dx >= dy:
        inc_yr = 0
        inc_xr = inc_xi
    else:
        inc_xr = 0
        inc_yr = inc_yi
        # Intercambio para reutilizar el bucle 
        dx, dy = dy, dx
        
    # 3 - Inicializar valores
    x, y = x1, y1
    av_r = 2 * dy
    av = av_r - dx
    av_i = av - dx
    
    # 4 - Bucle para trazado
    # Usamos un bucle que corra 'dx' veces (que ahora es el eje mayor)
    for _ in range(dx + 1):
        suma_gris += imagen[y][x]  # Sumar el nivel de gris del pixel actual
        total_pixeles += 1
        
        if av >= 0:
            x += inc_xi
            y += inc_yi
            av += av_i
        else:
            x += inc_xr
            y += inc_yr
            av += av_r

    return suma_gris / total_pixeles if total_pixeles > 0 else 0

def generar_lineas(marco_clavos, imagen, clavos, iteraciones):
    numero= random.randint(0, clavos)
    max_gris = 255
    numero = numero - marco_clavos.clavos_arriba.__len__()
    max_linea = None
    iter = 1
    list_lineas = []
    if numero < 0:
        numero = numero + marco_clavos.clavos_arriba.__len__()
        clavo_inicio = marco_clavos.clavos_arriba[numero]
        for clavo_fin in marco_clavos.clavos_abajo + marco_clavos.clavos_izquierda + marco_clavos.clavos_derecha:
                iter = iter + 1
                gris_local = nivel_gris_bresenham(clavo_inicio, clavo_fin, imagen)
                if (max_gris > gris_local):
                    max_linea = Linea(clavo_inicio, clavo_fin, gris_local)
                    max_gris = gris_local
                if (iter == 30):
                        list_lineas.append(max_linea)
                        iter = 1
                        max_gris = 255 
    else:
        numero = numero - marco_clavos.clavos_abajo.__len__()
        if numero < 0:
            numero = numero + marco_clavos.clavos_abajo.__len__()
            clavo_inicio = marco_clavos.clavos_abajo[numero]
            for clavo_fin in marco_clavos.clavos_arriba + marco_clavos.clavos_izquierda + marco_clavos.clavos_derecha:
                iter = iter + 1
                gris_local = nivel_gris_bresenham(clavo_inicio, clavo_fin, imagen)
                if (max_gris > gris_local):
                    max_linea = Linea(clavo_inicio, clavo_fin, gris_local)
                    max_gris = gris_local
                if (iter == 30):
                        list_lineas.append(max_linea)
                        iter = 1
                        max_gris = 255 
        else:
            numero = numero - marco_clavos.clavos_izquierda.__len__()
            if numero < 0:
                numero = numero + marco_clavos.clavos_izquierda.__len__()
                clavo_inicio = marco_clavos.clavos_izquierda[numero]
                for clavo_fin in marco_clavos.clavos_arriba + marco_clavos.clavos_abajo + marco_clavos.clavos_derecha:
                    iter = iter + 1
                    gris_local = nivel_gris_bresenham(clavo_inicio, clavo_fin, imagen)
                    if (max_gris > gris_local):
                        max_linea = Linea(clavo_inicio, clavo_fin, gris_local)
                        max_gris = gris_local
                    if (iter == 30):
                            list_lineas.append(max_linea)
                            iter = 1
                            max_gris = 255 
            else:
                numero = numero - marco_clavos.clavos_derecha.__len__()
                if numero < 0:
                    numero = numero + marco_clavos.clavos_derecha.__len__()
                    clavo_inicio = marco_clavos.clavos_derecha[numero]
                    for clavo_fin in marco_clavos.clavos_arriba + marco_clavos.clavos_abajo + marco_clavos.clavos_izquierda:
                        iter = iter + 1
                        gris_local = nivel_gris_bresenham(clavo_inicio, clavo_fin, imagen)
                        if (max_gris > gris_local):
                            max_linea = Linea(clavo_inicio, clavo_fin, gris_local)
                            max_gris = gris_local
                        if (iter == 30):
                            list_lineas.append(max_linea)
                            iter = 1
                            max_gris = 255 
    return list_lineas

def bresenham_dibujo(linea, imagen_resultado, imagen):
    x1, y1 = linea.clavo_inicio.x, linea.clavo_inicio.y
    x2, y2 = linea.clavo_fin.x, linea.clavo_fin.y
    suma_gris = 0.0
    total_pixeles = 0.0
    # 0 - Distancias
    dy = y2 - y1
    dx = x2 - x1
    
    # 1 - Incrementos para secciones con avance inclinado
    inc_yi = 1 if dy >= 0 else -1
    dy = abs(dy)
    
    inc_xi = 1 if dx >= 0 else -1
    dx = abs(dx)
    
    # 2 - Incrementos para secciones con avance recto
    if dx >= dy:
        inc_yr = 0
        inc_xr = inc_xi
    else:
        inc_xr = 0
        inc_yr = inc_yi
        # Intercambio para reutilizar el bucle 
        dx, dy = dy, dx
        
    # 3 - Inicializar valores
    x, y = x1, y1
    av_r = 2 * dy
    av = av_r - dx
    av_i = av - dx
    
    # 4 - Bucle para trazado
    # Usamos un bucle que corra 'dx' veces (que ahora es el eje mayor)
    for _ in range(dx + 1):
        imagen_resultado[y][x] = max(0, imagen_resultado[y][x] - (linea.nivel_gris*0.005))  # Reducir el nivel de gris del pixel actual para "dibujar" la línea
        imagen[y][x] = min(255, imagen[y][x] + 2)  # Aumentar el nivel de gris del pixel actual para "dibujar" la línea
        if av >= 0:
            x += inc_xi
            y += inc_yi
            av += av_i
        else:
            x += inc_xr
            y += inc_yr
            av += av_r
    
def dibujar_lineas(linea, imagen_resultado, imagen):
    bresenham_dibujo(linea,imagen_resultado, imagen)

def main(args):
    clavos = int(args[0])
    hilos = int(args[1])
    optimizaciones = int(args[2])
    imagen = args[3]
    resultado = args[4]
    imagen = converter_to_matrix(imagen)
    imagenResultado = np.full((MARCO, MARCO), 255, dtype=np.uint8)
    resultado_numerico = Resultado([])
    inicio = time.time()
    ultimo_print = inicio
    while resultado_numerico.lineas.__len__() < hilos:
        lista_lineas = generar_lineas(posicionar_clavos(clavos), imagen, clavos, optimizaciones)
        for linea in lista_lineas:
          if linea is not None and linea not in resultado_numerico.lineas:
            dibujar_lineas(linea, imagenResultado, imagen)
            resultado_numerico.lineas.append(linea)
            actual = len(resultado_numerico.lineas)
            ahora = time.time()

            if ahora - ultimo_print >= 1:   # imprime cada ~1 segundo
                porcentaje = (actual / hilos) * 100
                tiempo_transcurrido = ahora - inicio
                velocidad = actual / tiempo_transcurrido if tiempo_transcurrido > 0 else 0

                print(
                    f"Líneas: {actual}/{hilos} "
                    f"({porcentaje:4.1f}%) | "
                    f"Tiempo: {tiempo_transcurrido:6.1f}s | "
                    f"{velocidad:5.1f} líneas/s"
                )

                ultimo_print = ahora

    Image.fromarray(imagenResultado).save(resultado)
    
if __name__ == "__main__":  
    main(sys.argv[1:])


    
    

        
        
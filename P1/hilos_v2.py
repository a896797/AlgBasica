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
    img = img.resize((MARCO, MARCO), Image.Resampling.LANCZOS)
    img_matrix = np.array(img, dtype=np.int32) # Forzar int32 evita desbordamientos
    return img_matrix
    
def posicionar_clavos(Nclavos):
    resto4 = Nclavos % 4
    base = Nclavos // 4
    clavos_arriba = base
    clavos_abajo = base
    clavos_izquierda = base
    clavos_derecha = base

    if resto4 == 1:
        clavos_arriba += 1
    elif resto4 == 2:
        clavos_arriba += 1
        clavos_abajo += 1
    elif resto4 == 3:
        clavos_arriba += 1
        clavos_abajo += 1
        clavos_izquierda += 1

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
    
    dy = y2 - y1
    dx = x2 - x1
    
    inc_yi = 1 if dy >= 0 else -1
    dy = abs(dy)
    
    inc_xi = 1 if dx >= 0 else -1
    dx = abs(dx)
    
    if dx >= dy:
        inc_yr = 0
        inc_xr = inc_xi
    else:
        inc_xr = 0
        inc_yr = inc_yi
        dx, dy = dy, dx
        
    x, y = x1, y1
    av_r = 2 * dy
    av = av_r - dx
    av_i = av - dx
    
    for _ in range(dx + 1):
        suma_gris += imagen[y][x]
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

# =====================================================================
# GENERACIÓN VORAZ OPTIMIZADA (MÁXIMA VELOCIDAD)
# =====================================================================
def generar_lineas(marco_clavos, imagen, clavos, optimizaciones):
    # 1. Seleccionar una arista de inicio al azar y un clavo dentro de ella
    aristas = [marco_clavos.clavos_arriba, marco_clavos.clavos_abajo, 
               marco_clavos.clavos_izquierda, marco_clavos.clavos_derecha]
    aristas_validas = [a for a in aristas if len(a) > 0]
    
    arista_inicio = random.choice(aristas_validas)
    clavo_inicio = random.choice(arista_inicio)
    
    # 2. Agrupar todos los clavos de las OTRAS aristas para no conectar la misma pared
    destinos_posibles = []
    for arista in aristas_validas:
        if arista is not arista_inicio:
            destinos_posibles.extend(arista)
            
    if not destinos_posibles:
        return []
        
    # 3. EL TRUCO: Mismo volumen de trabajo que tu script original (30 candidatos)
    # Esto garantiza que el bucle de Python sea diminuto y ultrarrápido
    num_candidatos = 30
    destinos_candidatos = random.sample(destinos_posibles, min(num_candidatos, len(destinos_posibles)))
    
    list_lineas = []
    for clavo_fin in destinos_candidatos:
        gris_local = nivel_gris_bresenham(clavo_inicio, clavo_fin, imagen)
        list_lineas.append(Linea(clavo_inicio, clavo_fin, gris_local))

    # 4. Ordenamos el grupo de 30 y extraemos los mejores según dicte 'optimizaciones'
    list_lineas.sort(key=lambda l: l.nivel_gris)
    return list_lineas[:max(1, optimizaciones)]

def bresenham_dibujo(linea, imagen_resultado, imagen):
    x1, y1 = linea.clavo_inicio.x, linea.clavo_inicio.y
    x2, y2 = linea.clavo_fin.x, linea.clavo_fin.y
    
    dy = y2 - y1
    dx = x2 - x1
    
    inc_yi = 1 if dy >= 0 else -1
    dy = abs(dy)
    
    inc_xi = 1 if dx >= 0 else -1
    dx = abs(dx)
    
    if dx >= dy:
        inc_yr = 0
        inc_xr = inc_xi
    else:
        inc_xr = 0
        inc_yr = inc_yi
        dx, dy = dy, dx
        
    x, y = x1, y1
    av_r = 2 * dy
    av = av_r - dx
    av_i = av - dx
    
    for _ in range(dx + 1):
        # Operaciones seguras limitadas con min/max
        imagen_resultado[y][x] = max(0, int(imagen_resultado[y][x] - ((255 - linea.nivel_gris) * 0.05)))
        imagen[y][x] = min(255, imagen[y][x] + 2)
        if av >= 0:
            x += inc_xi
            y += inc_yi
            av += av_i
        else:
            x += inc_xr
            y += inc_yr
            av += av_r
    
def dibujar_lineas(linea, imagen_resultado, imagen):
    bresenham_dibujo(linea, imagen_resultado, imagen)

def main(args):
    clavos = int(args[0])
    hilos = int(args[1])
    optimizaciones = int(args[2])
    imagen_path = args[3]
    resultado_path = args[4]
    
    imagen = converter_to_matrix(imagen_path)
    imagenResultado = np.full((MARCO, MARCO), 255, dtype=np.int32) # Usar int32 internamente para evitar desbordamientos
    resultado_numerico = Resultado([])
    
    # Precalculo estático fuera del bucle para ahorrar tiempo
    marco_clavos_estatico = posicionar_clavos(clavos)
    
    inicio = time.time()
    ultimo_print = inicio
    
    while len(resultado_numerico.lineas) < hilos:
        lista_lineas = generar_lineas(marco_clavos_estatico, imagen, clavos, optimizaciones)
        
        for linea in lista_lineas:
            if len(resultado_numerico.lineas) >= hilos:
                break
                
            if linea is not None and linea not in resultado_numerico.lineas:
                dibujar_lineas(linea, imagenResultado, imagen)
                resultado_numerico.lineas.append(linea)
                actual = len(resultado_numerico.lineas)
                ahora = time.time()

                if ahora - ultimo_print >= 1:
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

    # Convertir a uint8 únicamente al guardar la imagen
    Image.fromarray(imagenResultado.astype(np.uint8)).save(resultado_path)
    
if __name__ == "__main__":  
    main(sys.argv[1:])
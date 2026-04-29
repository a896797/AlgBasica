#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests adicionales: Casos extremos y patrones especiales
Para análisis avanzado en memoria
"""

import sys
from pathlib import Path

# Importar funciones del módulo principal
sys.path.insert(0, str(Path(__file__).parent))
from formarEquipos import leer_matrices_entrada, media_matriz, generar_todas_las_soluciones
import time

def generar_matriz_identidad(n):
    """Matriz con ceros en diagonal (sin conflicto consigo mismo)."""
    return [[0 if i == j else 1 for j in range(n)] for i in range(n)]

def generar_matriz_uniforme(n, valor=5):
    """Matriz donde todos los elementos son iguales (excepto diagonal)."""
    return [[0 if i == j else valor for j in range(n)] for i in range(n)]

def generar_matriz_triangular(n):
    """Matriz triangular: conflictos aumentan en diagonal."""
    return [[0 if i == j else i + j for j in range(n)] for i in range(n)]

def generar_matriz_aleatoria_baja(n):
    """Matriz con conflictos bajos."""
    import random
    random.seed(42)
    return [[0 if i == j else random.randint(0, 2) for j in range(n)] for i in range(n)]

def ejecutar_caso_prueba(nombre, matriz):
    """Ejecuta un caso de prueba y retorna estadísticas."""
    n = len(matriz)
    print(f"\n{'─' * 70}")
    print(f"Caso: {nombre}")
    print(f"Tamaño: N={n} ({n//3} equipos)")
    print(f"{'─' * 70}")
    
    try:
        media = media_matriz(matriz)
        participantes = list(range(n))
        
        print(f"Media de matriz: {media:.2f}")
        print("Ejecutando búsqueda...")
        
        inicio = time.perf_counter()
        valor_optimo, nodos = generar_todas_las_soluciones(
            participantes, 
            matriz, 
            media
        )
        fin = time.perf_counter()
        
        tiempo_ms = (fin - inicio) * 1000
        
        print(f"✓ Tiempo: {tiempo_ms:.3f} ms")
        print(f"✓ Nodos: {nodos}")
        print(f"✓ Valor óptimo: {valor_optimo}")
        
        if tiempo_ms > 0:
            print(f"✓ Nodos/ms: {nodos/tiempo_ms:.0f}")
        
        return {
            "nombre": nombre,
            "n": n,
            "tiempo_ms": tiempo_ms,
            "nodos": nodos,
            "valor_optimo": valor_optimo,
            "media": media
        }
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def main():
    """Ejecuta suite de pruebas adicionales."""
    
    print("\n" + "=" * 70)
    print("PRUEBAS ADICIONALES - CASOS EXTREMOS Y PATRONES ESPECIALES".center(70))
    print("=" * 70)
    
    resultados = []
    
    # Caso 1: Matriz uniforme (todos igual conflicto)
    resultado = ejecutar_caso_prueba(
        "Matriz Uniforme (N=6)",
        generar_matriz_uniforme(6, 3)
    )
    if resultado:
        resultados.append(resultado)
    
    # Caso 2: Matriz identidad (sin conflicto consigo)
    resultado = ejecutar_caso_prueba(
        "Matriz Identidad (N=6)",
        generar_matriz_identidad(6)
    )
    if resultado:
        resultados.append(resultado)
    
    # Caso 3: Matriz triangular (conflictos crecientes)
    resultado = ejecutar_caso_prueba(
        "Matriz Triangular (N=9)",
        generar_matriz_triangular(9)
    )
    if resultado:
        resultados.append(resultado)
    
    # Caso 4: Matriz con conflictos muy bajos
    resultado = ejecutar_caso_prueba(
        "Matriz Baja (N=9)",
        generar_matriz_aleatoria_baja(9)
    )
    if resultado:
        resultados.append(resultado)
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN COMPARATIVO")
    print("=" * 70)
    
    print(f"\n{'Caso':<30} {'N':>4} {'Tiempo (ms)':>12} {'Nodos':>10} {'Valor':>10}")
    print("─" * 70)
    
    for r in resultados:
        print(
            f"{r['nombre']:<30} {r['n']:>4} "
            f"{r['tiempo_ms']:>12.3f} {r['nodos']:>10} {r['valor_optimo']:>10}"
        )
    
    print("─" * 70)
    
    # Análisis de complejidad
    print("\n" + "=" * 70)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("=" * 70)
    
    tiempo_total = sum(r['tiempo_ms'] for r in resultados)
    nodos_total = sum(r['nodos'] for r in resultados)
    
    print(f"Tiempo total: {tiempo_total:.3f} ms")
    print(f"Nodos total: {nodos_total}")
    print(f"Promedio de nodos/ms: {nodos_total/tiempo_total:.0f}")
    
    print("\n✓ Pruebas completadas exitosamente")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

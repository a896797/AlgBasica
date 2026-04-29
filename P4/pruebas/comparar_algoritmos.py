#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de análisis comparativo entre Backtracking y Programación Lineal
Para la memoria de P4
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path

P4_ROOT = Path(__file__).resolve().parent.parent
PRUEBAS_DIR = Path(__file__).resolve().parent

def ejecutar_algoritmo(script_path, entrada, algoritmo_nombre):
    """Ejecuta un algoritmo y retorna los resultados."""
    salida_temp = PRUEBAS_DIR / f"salida_{algoritmo_nombre}.txt"
    
    print(f"\n{'=' * 80}")
    print(f"Ejecutando: {algoritmo_nombre.upper()}")
    print(f"{'=' * 80}")
    
    try:
        inicio = time.perf_counter()
        
        resultado = subprocess.run(
            [sys.executable, str(script_path), str(entrada), str(salida_temp)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        fin = time.perf_counter()
        tiempo_total = (fin - inicio) * 1000
        
        print(resultado.stdout)
        
        if resultado.returncode != 0:
            print(f"⚠️  Error: {resultado.stderr}")
            return None
        
        return {
            "algoritmo": algoritmo_nombre,
            "tiempo_total_ms": tiempo_total,
            "archivo_salida": str(salida_temp),
            "exitoso": True
        }
        
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout (>120s) en {algoritmo_nombre}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Ejecuta análisis comparativo."""
    
    entrada = PRUEBAS_DIR / "pruebas_memoria.txt"
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + "ANÁLISIS COMPARATIVO - FORMACIÓN DE EQUIPOS".center(78) + "║")
    print("║" + "Backtracking vs Programación Lineal".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    
    if not entrada.exists():
        print(f"❌ Error: {entrada} no existe")
        return False
    
    print(f"\n📥 Archivo de entrada: {entrada}")
    
    # Ejecutar ambos algoritmos
    resultados = []
    
    # Backtracking
    resultado_bt = ejecutar_algoritmo(
        P4_ROOT / "formarEquipos.py",
        entrada,
        "backtracking"
    )
    if resultado_bt:
        resultados.append(resultado_bt)
    
    # Programación Lineal
    resultado_pl = ejecutar_algoritmo(
        P4_ROOT / "programacion_lineal.py",
        entrada,
        "programacion_lineal"
    )
    if resultado_pl:
        resultados.append(resultado_pl)
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN COMPARATIVO")
    print("=" * 80)
    
    if resultados:
        for r in resultados:
            print(f"\n{r['algoritmo'].upper()}:")
            print(f"  ⏱️  Tiempo total: {r['tiempo_total_ms']:.2f} ms")
            print(f"  📤 Salida: {r['archivo_salida']}")

        if len(resultados) == 2:
            bt_tiempo = resultados[0]['tiempo_total_ms']
            pl_tiempo = resultados[1]['tiempo_total_ms']
            ratio = max(bt_tiempo, pl_tiempo) / min(bt_tiempo, pl_tiempo)
            mas_rapido = "BT" if bt_tiempo < pl_tiempo else "PL"

            print(f"\n📈 Análisis:")
            print(f"  {mas_rapido} es {ratio:.2f}x más rápido")
            print(f"  Diferencia: {abs(bt_tiempo - pl_tiempo):.2f} ms")
        else:
            print("\n❌ No se completó la comparación completa")
            print("   Falta al menos una de las dos ejecuciones requeridas")
            return False
    else:
        print("❌ No se completaron pruebas exitosas")
        return False
    
    print("\n" + "=" * 80)
    print("✅ Análisis completado")
    print("=" * 80 + "\n")
    
    return True

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)

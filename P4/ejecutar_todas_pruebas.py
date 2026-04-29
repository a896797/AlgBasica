#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script maestro - Ejecuta todas las pruebas de P4
Mantiene la estructura limpia ejecutando scripts de la carpeta pruebas/
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def ejecutar_script(script_path, descripcion):
    """Ejecuta un script Python y muestra resultados."""
    print(f"\n{'=' * 80}")
    print(f"▶️  {descripcion}")
    print(f"{'=' * 80}\n")
    
    try:
        resultado = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(script_path.parent),
            timeout=120
        )
        return resultado.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"\n❌ Timeout: {descripcion} tardó demasiado (>120s)")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Ejecuta suite completa de pruebas."""
    
    base_path = Path(__file__).parent
    pruebas_path = base_path / "pruebas"
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + "SUITE COMPLETA DE PRUEBAS - P4".center(78) + "║")
    print("║" + "Formación de Equipos: Backtracking vs Programación Lineal".center(78) + "║")
    print("╚" + "=" * 78 + "╝\n")
    
    if not pruebas_path.exists():
        print(f"❌ Error: La carpeta {pruebas_path} no existe")
        return False
    
    resultados = []
    inicio_total = time.perf_counter()
    
    # Prueba 1: Pruebas principales (4 casos)
    script1 = pruebas_path / "ejecutar_pruebas_memoria.py"
    if script1.exists():
        exito = ejecutar_script(
            script1,
            "1/3 - Pruebas Principales (N=3,6,9,12)"
        )
        resultados.append(("Pruebas Principales", exito))
    
    # Prueba 2: Pruebas adicionales (casos extremos)
    script2 = pruebas_path / "pruebas_adicionales.py"
    if script2.exists():
        exito = ejecutar_script(
            script2,
            "2/3 - Pruebas Adicionales (Casos Extremos)"
        )
        resultados.append(("Pruebas Adicionales", exito))
    
    # Prueba 3: Comparativa BT vs PL
    script3 = pruebas_path / "comparar_algoritmos.py"
    if script3.exists():
        exito = ejecutar_script(
            script3,
            "3/3 - Análisis Comparativo (Backtracking vs PL)"
        )
        resultados.append(("Comparativa Algoritmos", exito))
    
    fin_total = time.perf_counter()
    tiempo_total = (fin_total - inicio_total) * 1000
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL DE PRUEBAS")
    print("=" * 80)
    
    exitosas = sum(1 for _, exito in resultados if exito)
    total = len(resultados)
    
    print(f"\n{'Prueba':<35} {'Estado':>20}")
    print("─" * 80)
    
    for nombre, exito in resultados:
        estado = "✅ EXITOSA" if exito else "❌ FALLIDA"
        print(f"{nombre:<35} {estado:>20}")
    
    print("─" * 80)
    print(f"{'TOTAL':<35} {exitosas}/{total} EXITOSAS")
    print(f"{'Tiempo total':<35} {tiempo_total:.2f} ms")
    print("=" * 80)
    
    if exitosas == total:
        print("\n✅ Todas las pruebas completadas exitosamente")
        print(f"📂 Los resultados están en: pruebas/")
        print("=" * 80 + "\n")
        return True
    else:
        print(f"\n⚠️  {total - exitosas} prueba(s) fallida(s)")
        print("=" * 80 + "\n")
        return False

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)

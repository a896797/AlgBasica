#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas comprehensivas para P4 - Formación de Equipos
Ejecuta múltiples casos de prueba y genera estadísticas para la memoria
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def ejecutar_pruebas():
    """Ejecuta las pruebas de memoria y genera estadísticas."""
    
    script_path = Path(__file__).parent / "formarEquipos.py"
    entrada = Path(__file__).parent / "pruebas_memoria.txt"
    salida_temp = Path(__file__).parent / "salida_pruebas_memoria.txt"
    
    print("=" * 80)
    print("PRUEBAS COMPREHENSIVAS - FORMACIÓN DE EQUIPOS")
    print("=" * 80)
    print()
    
    if not entrada.exists():
        print(f"❌ Error: No existe el archivo {entrada}")
        return False
    
    print(f"📝 Ejecutando: {script_path}")
    print(f"📥 Entrada: {entrada}")
    print(f"📤 Salida: {salida_temp}")
    print()
    
    try:
        inicio_total = time.perf_counter()
        
        # Ejecutar el script
        resultado = subprocess.run(
            [sys.executable, str(script_path), str(entrada), str(salida_temp)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        fin_total = time.perf_counter()
        tiempo_total = (fin_total - inicio_total) * 1000
        
        # Mostrar salida estándar
        print(resultado.stdout)
        
        if resultado.returncode != 0:
            print(f"❌ Error en la ejecución:")
            print(resultado.stderr)
            return False
        
        # Mostrar resultados finales
        print()
        print("=" * 80)
        print(f"✅ Prueba completada exitosamente")
        print(f"⏱️  Tiempo total: {tiempo_total:.2f} ms")
        print("=" * 80)
        
        # Leer y mostrar archivo de salida
        if salida_temp.exists():
            print()
            print("📊 Contenido de salida:")
            with open(salida_temp, 'r', encoding='utf-8') as f:
                print(f.read())
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Error: La ejecución tardó demasiado (>60s)")
        return False
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        return False

if __name__ == "__main__":
    exito = ejecutar_pruebas()
    sys.exit(0 if exito else 1)

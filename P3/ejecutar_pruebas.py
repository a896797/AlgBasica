import subprocess
import os
from pathlib import Path

def ejecutar_todas_pruebas(directorio_pruebas, fichero_salida, formato=0):
    """
    Ejecuta ubicaCentros.py con todas las entradas de la carpeta pruebas.
    
    Args:
        directorio_pruebas: Ruta a la carpeta con los archivos de entrada
        fichero_salida: Archivo donde guardar todas las salidas combinadas
        formato: 0 = sin poda, 1 = con poda
    """
    
    # Obtener todos los archivos .txt de la carpeta pruebas
    archivos_entrada = sorted([f for f in os.listdir(directorio_pruebas) if f.endswith('.txt')])
    
    if not archivos_entrada:
        print(f"No se encontraron archivos .txt en {directorio_pruebas}")
        return
    
    print(f"Se encontraron {len(archivos_entrada)} archivos de entrada\n")
    print("=" * 80)
    
    todas_salidas = []
    
    for i, archivo in enumerate(archivos_entrada, 1):
        ruta_entrada = os.path.join(directorio_pruebas, archivo)
        # Crear archivo temporal para la salida de este caso
        ruta_salida_temp = os.path.join(directorio_pruebas, f"temp_{archivo}")
        
        print(f"\n[{i}/{len(archivos_entrada)}] Procesando: {archivo}")
        print("-" * 80)
        
        try:
            # Ejecutar ubicaCentros.py
            cmd = ["python", "ubicaCentros.py", ruta_entrada, ruta_salida_temp, str(formato)]
            resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if resultado.returncode != 0:
                print(f"❌ Error al ejecutar con {archivo}")
                print(f"Error: {resultado.stderr}")
                todas_salidas.append(f"ARCHIVO: {archivo}\nERROR: {resultado.stderr}")
            else:
                # Leer la salida del programa
                try:
                    with open(ruta_salida_temp, 'r') as f:
                        salida = f.read().strip()
                    
                    # Mostrar por pantalla
                    print(f"✓ Archivo: {archivo}")
                    print(f"Resultados:")
                    print(salida)
                    
                    # Guardar para el archivo final
                    todas_salidas.append(f"ARCHIVO: {archivo}\n{salida}")
                    
                    # Limpiar archivo temporal
                    os.remove(ruta_salida_temp)
                except Exception as e:
                    print(f"Error al leer salida: {e}")
                    todas_salidas.append(f"ARCHIVO: {archivo}\nERROR AL LEER SALIDA: {e}")
        
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout ejecutando {archivo}")
            todas_salidas.append(f"ARCHIVO: {archivo}\nERROR: TIMEOUT")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            todas_salidas.append(f"ARCHIVO: {archivo}\nERROR: {e}")
    
    # Guardar todas las salidas en un archivo
    print("\n" + "=" * 80)
    print(f"\nGuardando salidas en {fichero_salida}...")
    
    with open(fichero_salida, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DE TODAS LAS PRUEBAS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Formato: {'Sin poda (0)' if formato == 0 else 'Con poda (1)'}\n")
        f.write("=" * 80 + "\n\n")
        f.write(("\n\n" + "-" * 80 + "\n\n").join(todas_salidas))
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("FIN DE LOS RESULTADOS\n")
    
    print(f"✓ Salidas guardadas en {fichero_salida}")
    print(f"\nProceso completado. {len(archivos_entrada)} archivos procesados.")


if __name__ == "__main__":
    import sys
    
    # Rutas
    dir_pruebas = os.path.join(os.path.dirname(__file__), 'pruebas')
    archivo_salida = os.path.join(os.path.dirname(__file__), 'salida_todas_pruebas.txt')
    
    # Formato por defecto es sin poda (0), o con poda (1) si se pasa como argumento
    formato = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    ejecutar_todas_pruebas(dir_pruebas, archivo_salida, formato)

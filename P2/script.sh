#!/bin/bash

# Carpeta donde están los archivos .txt
DIR_PRUEBAS="pruebas"

# Comprobamos si se ha pasado al menos la variante
if [ -z "$1" ]; then
    echo "Uso: $0 <variante 0|1|2|3> [archivo_diccionario] [archivo_texto]"
    echo "Si omite el archivo_texto, se ejecutara el modo experimento aleatorio."
    exit 1
fi

VARIANTE_IN=$1

# --- CASO ESPECIAL: VARIANTE 0 (TODAS LAS COMBINACIONES) ---
if [ "$VARIANTE_IN" == "0" ]; then
    echo "======================================================"
    echo "MODO AUTOMATICO: Ejecutando todas las combinaciones"
    echo "======================================================"
    
    for V in 1 2 3; do
        echo ""
        echo "--- PROBANDO ALGORITMO: VARIANTE $V ---"
        for D in 1 2 3; do
            # Añadimos la ruta de la carpeta pruebas
            DICC="${DIR_PRUEBAS}/diccionario${D}.txt"
            for T in 1 2; do
                TXT="${DIR_PRUEBAS}/texto${D}.${T}.txt"
                
                if [ -f "$DICC" ]; then
                    if [ -f "$TXT" ]; then
                        # Leemos la primera línea del archivo de texto
                        CONTENIDO=$(head -n 1 "$TXT")
                        echo "[Ejecutando] Var $V | $DICC | $TXT"
                        python3 separarPalabras.py "$V" "$DICC" "$CONTENIDO"
                        echo "--------------------------------------------------"
                    else
                        echo "[Aviso] No se encuentra $TXT"
                    fi
                else
                    echo "[Aviso] No se encuentra $DICC"
                fi
            done
        done
    done
    exit 0
fi

# --- CASO NORMAL / EXPERIMENTO ALEATORIO ---
# Nota: Aquí el usuario debe pasar la ruta completa si lo lanza a mano
# Ejemplo: ./script.sh 1 pruebas/diccionario1.txt
DICCIONARIO=$2
ARCHIVO_TEXTO=$3

# Validamos que al menos exista el diccionario
if [ -z "$DICCIONARIO" ]; then
    echo "Error: Debe especificar al menos un diccionario."
    exit 1
fi

if [ ! -f "$DICCIONARIO" ]; then
    echo "Error: no existe $DICCIONARIO"
    exit 1
fi

# SI NO HAY ARCHIVO DE TEXTO -> MODO EXPERIMENTO (Tarea 3)
if [ -z "$ARCHIVO_TEXTO" ]; then
    echo ""
    echo "[MODO EXPERIMENTO] No se ha pasado texto."
    echo "Usando Variante: $VARIANTE_IN | Diccionario: $DICCIONARIO"
    echo "--------------------------------------------------"
    python3 tests_aleatorios.py "$VARIANTE_IN" "$DICCIONARIO"
    exit 0
fi

# SI HAY ARCHIVO DE TEXTO -> EJECUCION NORMAL
if [ ! -f "$ARCHIVO_TEXTO" ]; then
    echo "Error: no existe $ARCHIVO_TEXTO"
    exit 1
fi

TEXTO_INDIV=$(head -n 1 "$ARCHIVO_TEXTO")
echo "Ejecutando separarPalabras variante $VARIANTE_IN con $DICCIONARIO..."
python3 separarPalabras.py "$VARIANTE_IN" "$DICCIONARIO" "$TEXTO_INDIV"
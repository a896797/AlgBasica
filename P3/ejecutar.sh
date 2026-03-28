#!/bin/bash

set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROGRAMA="$SCRIPT_DIR/ubicaCentros.py"
DIR_PRUEBAS="$SCRIPT_DIR/pruebas"
SALIDA_GLOBAL="$SCRIPT_DIR/salida_todas_pruebas.txt"

if command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
else
  echo "Error: no se encontro python ni python3 en PATH."
  exit 1
fi

usage() {
  echo "Uso:"
  echo "  $0 <version>"
  echo "    - Ejecuta todos los tests de '$DIR_PRUEBAS'"
  echo "    - Guarda todo en '$SALIDA_GLOBAL'"
  echo ""
  echo "  $0 <entrada> <salida> <version>"
  echo "    - Ejecuta un unico caso"
  echo ""
  echo "version: 0 = sin poda, 1 = con poda"
}

validar_version() {
  local v="$1"
  if [ "$v" != "0" ] && [ "$v" != "1" ]; then
    echo "Error: version debe ser 0 o 1."
    exit 1
  fi
}

# Modo 1: solo version -> ejecutar todos los tests
if [ "$#" -eq 1 ]; then
  version="$1"
  validar_version "$version"

  if [ ! -d "$DIR_PRUEBAS" ]; then
    echo "Error: no existe la carpeta de pruebas: $DIR_PRUEBAS"
    exit 1
  fi

  # Lista de archivos .txt ordenada
  mapfile -t archivos < <(find "$DIR_PRUEBAS" -maxdepth 1 -type f -name "*.txt" | sort)

  if [ "${#archivos[@]}" -eq 0 ]; then
    echo "No se encontraron archivos .txt en $DIR_PRUEBAS"
    exit 1
  fi

  echo "Se encontraron ${#archivos[@]} archivos de entrada"
  echo
  printf '=%.0s' {1..80}
  echo

  {
    echo "RESULTADOS DE TODAS LAS PRUEBAS"
    printf '=%.0s' {1..80}
    echo
    if [ "$version" = "0" ]; then
      echo "Formato: Sin poda (0)"
    else
      echo "Formato: Con poda (1)"
    fi
    printf '=%.0s' {1..80}
    echo
    echo
  } > "$SALIDA_GLOBAL"

  total="${#archivos[@]}"
  idx=0

  for entrada in "${archivos[@]}"; do
    idx=$((idx + 1))
    nombre="$(basename "$entrada")"
    salida_tmp="$DIR_PRUEBAS/temp_${nombre}.out"

    echo "[$idx/$total] Procesando: $nombre"
    printf -- '-%.0s' {1..80}
    echo

    if "$PYTHON_CMD" "$PROGRAMA" "$entrada" "$salida_tmp" "$version"; then
      echo "Archivo: $nombre"
      if [ -f "$salida_tmp" ]; then
        cat "$salida_tmp"
      fi

      {
        echo "ARCHIVO: $nombre"
        if [ -f "$salida_tmp" ]; then
          cat "$salida_tmp"
        else
          echo "ERROR: no se genero archivo de salida temporal"
        fi
        echo
        printf -- '-%.0s' {1..80}
        echo
        echo
      } >> "$SALIDA_GLOBAL"
    else
      echo "Error ejecutando: $nombre"
      {
        echo "ARCHIVO: $nombre"
        echo "ERROR: fallo al ejecutar ubicaCentros.py"
        echo
        printf -- '-%.0s' {1..80}
        echo
        echo
      } >> "$SALIDA_GLOBAL"
    fi

    if [ -f "$salida_tmp" ]; then
      rm -f "$salida_tmp"
    fi

    echo
  done

  {
    printf '=%.0s' {1..80}
    echo
    echo "FIN DE LOS RESULTADOS"
  } >> "$SALIDA_GLOBAL"

  printf '=%.0s' {1..80}
  echo
  echo "Salidas guardadas en: $SALIDA_GLOBAL"
  echo "Proceso completado."
  exit 0
fi

# Modo 2: entrada salida version -> ejecutar un caso
if [ "$#" -eq 3 ]; then
  entrada="$1"
  salida="$2"
  version="$3"

  validar_version "$version"

  "$PYTHON_CMD" "$PROGRAMA" "$entrada" "$salida" "$version"
  exit $?
fi

usage
exit 1

#!/usr/bin/env bash

set -u

export PYTHONIOENCODING="utf-8"
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"

base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pruebas_dir="${base_dir}/pruebas"

run_script() {
    local script_path="$1"
    local descripcion="$2"

    printf '\n================================================================================\n'
    printf '>> %s\n' "$descripcion"
    printf '================================================================================\n\n'

    python3 "$script_path"
}

main() {
    printf '\n'
    printf '================================================================================\n'
    printf 'SUITE COMPLETA DE PRUEBAS - P4\n'
    printf 'Formacion de Equipos: Backtracking vs Programacion Lineal\n'
    printf '================================================================================\n\n'

    if [ ! -d "$pruebas_dir" ]; then
        printf 'Error: La carpeta %s no existe\n' "$pruebas_dir"
        return 1
    fi

    local total=0
    local exitosas=0
    local estado=0
    local resultado1=1
    local resultado2=1
    local resultado3=1

    local script1="${pruebas_dir}/ejecutar_pruebas_memoria.py"
    local script2="${pruebas_dir}/pruebas_adicionales.py"
    local script3="${pruebas_dir}/comparar_algoritmos.py"

    if [ -f "$script1" ]; then
        total=$((total + 1))
        if run_script "$script1" "1/3 - Pruebas Principales (N=3,6,9,12)"; then
            exitosas=$((exitosas + 1))
            resultado1=0
        else
            estado=1
        fi
    fi

    if [ -f "$script2" ]; then
        total=$((total + 1))
        if run_script "$script2" "2/3 - Pruebas Adicionales (Casos Extremos)"; then
            exitosas=$((exitosas + 1))
            resultado2=0
        else
            estado=1
        fi
    fi

    if [ -f "$script3" ]; then
        total=$((total + 1))
        if run_script "$script3" "3/3 - Analisis Comparativo (Backtracking vs PL)"; then
            exitosas=$((exitosas + 1))
            resultado3=0
        else
            estado=1
        fi
    fi

    printf '\n================================================================================\n'
    printf 'RESUMEN FINAL DE PRUEBAS\n'
    printf '================================================================================\n\n'

    printf '%-35s %20s\n' "Prueba" "Estado"
    printf '%-35s %20s\n' "-----------------------------------" "--------------------"

    if [ -f "$script1" ]; then
        printf '%-35s %20s\n' "Pruebas Principales" "$([ "$resultado1" -eq 0 ] && echo 'EXITOSA' || echo 'FALLIDA')"
    fi
    if [ -f "$script2" ]; then
        printf '%-35s %20s\n' "Pruebas Adicionales" "$([ "$resultado2" -eq 0 ] && echo 'EXITOSA' || echo 'FALLIDA')"
    fi
    if [ -f "$script3" ]; then
        printf '%-35s %20s\n' "Comparativa Algoritmos" "$([ "$resultado3" -eq 0 ] && echo 'EXITOSA' || echo 'FALLIDA')"
    fi

    printf '%-35s %20s\n' "TOTAL" "${exitosas}/${total} EXITOSAS"
    printf '================================================================================\n'

    if [ "$exitosas" -eq "$total" ] && [ "$total" -gt 0 ]; then
        printf '\nTodas las pruebas completadas exitosamente\n'
        printf 'Los resultados estan en: pruebas/\n'
        printf '================================================================================\n\n'
        return 0
    fi

    printf '\n%s prueba(s) fallida(s)\n' "$((total - exitosas))"
    printf '================================================================================\n\n'
    return "$estado"
}

main
# Carpeta de Pruebas - P4

Contiene todos los scripts y datos necesarios para probar la solución de Formación de Equipos.

## Estructura

```
pruebas/
├── pruebas_memoria.txt              # Datos de entrada (4 casos: N=3,6,9,12)
├── ejecutar_pruebas_memoria.py      # Pruebas principales con backtracking
├── pruebas_adicionales.py           # Casos extremos y patrones especiales
├── comparar_algoritmos.py           # Análisis comparativo BT vs PL
└── salida_*.txt                     # Archivos de salida generados
```

## Cómo Ejecutar

### Opción 1: Todas las pruebas a la vez (RECOMENDADO)

Desde la carpeta P4:
```bash
python ejecutar_todas_pruebas.py
```

### Opción 2: Pruebas individuales

Desde dentro de `pruebas/`:

```bash
# Pruebas principales (4 casos)
python ejecutar_pruebas_memoria.py

# Casos extremos y patrones
python pruebas_adicionales.py

# Comparativa de algoritmos
python comparar_algoritmos.py
```

### Opción 3: Desde PowerShell

```powershell
# Desde P4 - Ejecutar todo
python ejecutar_todas_pruebas.py

# O individual desde pruebas/
cd pruebas
python ejecutar_pruebas_memoria.py
```

## Archivos de Entrada

### `pruebas_memoria.txt`

Contiene 4 matrices de conflictos para diferentes tamaños:

| Caso | N  | Descripción |
|------|-----|-----------|
| 1    | 3  | Trivial (1 equipo) |
| 2    | 6  | Pequeño (2 equipos) |
| 3    | 9  | Intermedio (3 equipos) |
| 4    | 12 | Grande (4 equipos) |

## Resultados Esperados

Los scripts generarán archivos de salida:
- `salida_pruebas_memoria.txt`
- `salida_backtracking.txt`
- `salida_programacion_lineal.txt`

Y mostrarán en terminal:
- Tiempos de ejecución
- Número de nodos generados
- Valor óptimo encontrado
- Análisis comparativo

## Notas Importantes

- ⚠️ N=12 puede tomar ~66ms (exponencial)
- ✅ N≤9 es rápido (<2ms)
- 📊 Poda reduce búsqueda en factor ~944×

---

*Para la memoria, consulta MEMORIA_RESULTADOS.md en la carpeta padre (P4)*

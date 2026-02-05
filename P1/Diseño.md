# Algoritmo de Arte con Hilos

## Especificación del Problema

**Entrada:** Matriz de píxeles + Conjunto de clavos

**Salida:** Conjunto de pares de clavos (hilos) + Nivel de gris de cada hilo (0-255)

---

## Descripción General del Programa

1. Encontrar las posibles líneas dibujables
2. Seleccionar la más adecuada
3. Dibujarla
4. Eliminarla de la imagen

---

## 1. Heurística para el Algoritmo Voraz

### 1.1 Paso 1: Selección de Líneas Candidatas

**Opción A:**
- Elegir un clavo y evaluar todas las líneas dibujables desde él

**Opción B:**
- Elegir un cierto número de parejas aleatorias de clavos
- Evaluar las líneas que las conectan

### 1.2 Paso 2: Selección de la Mejor Línea

- Definir una función de error y minimizarla
- Elegir la línea más oscura

---

## 2. Condiciones de Parada

- Se han dibujado una cierta cantidad de hilos
- Al añadir un nuevo hilo no se reduce el error global
- El error total alcanza un cierto umbral

---

## 3. Reducción del Tiempo de Ejecución

Se selecciona un subconjunto de $c$ hilos, donde $0 \leq c \leq n$. En cada iteración se elige el mejor/mejores hilo(s).

---

## 4. Algoritmo para la Selección de Líneas

Utilizar el **algoritmo de Bresenham** para determinar qué píxeles componen cada línea.

## 5. Bibliografía

https://aprendeconalf.es/docencia/python/manual/numpy/



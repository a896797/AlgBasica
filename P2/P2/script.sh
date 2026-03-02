# Comprobamos que se pasan los parametros correctos
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <variante 1|2|3> <archivo_texto>"
    exit 1
fi

VARIANTE=$1
ARCHIVO_TEXTO=$2

# Validamos variante
if [[ "$VARIANTE" != "1" && "$VARIANTE" != "2" && "$VARIANTE" != "3" ]]; then
    echo "Error: la variante debe ser 1, 2 o 3"
    exit 1
fi

# Seleccionamos el diccionario segun la variante
DICCIONARIO="diccionario$VARIANTE.txt"

# Comprobamos que existan los archivos
if [ ! -f "$DICCIONARIO" ]; then
    echo "Error: no existe el diccionario $DICCIONARIO"
    exit 1
fi

if [ ! -f "$ARCHIVO_TEXTO" ]; then
    echo "Error: no existe el archivo de texto $ARCHIVO_TEXTO"
    exit 1
fi

# Ejecutamos el programa
echo "Ejecutando separarPalabras variante $VARIANTE con $DICCIONARIO y $ARCHIVO_TEXTO..."
python3 separarPalabras.py "$VARIANTE" "$DICCIONARIO" $(cat "$ARCHIVO_TEXTO")

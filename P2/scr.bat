@echo off
setlocal enabledelayedexpansion

:: Comprobamos si se ha pasado al menos la variante
if "%~1" == "" (
    echo Uso: %~0 ^<variante 0^|1^|2^|3^> [archivo_diccionario] [archivo_texto]
    echo Si omite el archivo_texto, se ejecutara el modo experimento aleatorio.
    exit /b 1
)

set VARIANTE_IN=%~1

:: --- CASO ESPECIAL: VARIANTE 0 (TODAS LAS COMBINACIONES) ---
if "%VARIANTE_IN%"=="0" (
    echo ======================================================
    echo MODO AUTOMATICO: Ejecutando todas las combinaciones
    echo ======================================================
    
    for %%V in (1 2 3) do (
        echo.
        echo --- PROBANDO ALGORITMO: VARIANTE %%V ---
        for %%D in (1 2 3) do (
            set "DICC=diccionario%%D.txt"
            for %%T in (1 2) do (
                set "TXT=texto%%D.%%T.txt"
                if exist "!DICC!" (
                    if exist "!TXT!" (
                        set /p CONTENIDO=<"!TXT!"
                        echo [Ejecutando] Var %%V ^| !DICC! ^| !TXT!
                        python separarPalabras.py "%%V" "!DICC!" "!CONTENIDO!"
                        echo --------------------------------------------------
                    ) else (
                        echo [Aviso] No se encuentra !TXT!
                    )
                ) else (
                    echo [Aviso] No se encuentra !DICC!
                )
            )
        )
    )
    goto :fin
)

:: --- CASO NORMAL / EXPERIMENTO ALEATORIO ---
set DICCIONARIO=%~2
set ARCHIVO_TEXTO=%~3

:: Validamos que al menos exista el diccionario
if "%DICCIONARIO%"=="" (
    echo Error: Debe especificar al menos un diccionario.
    exit /b 1
)
if not exist "%DICCIONARIO%" (echo Error: no existe %DICCIONARIO% & exit /b 1)

:: SI NO HAY ARCHIVO DE TEXTO -> MODO EXPERIMENTO (Tarea 3)
if "%ARCHIVO_TEXTO%"=="" (
    echo.
    echo [MODO EXPERIMENTO] No se ha pasado texto.
    echo Usando Variante: %VARIANTE_IN% ^| Diccionario: %DICCIONARIO%
    echo --------------------------------------------------
    :: Pasamos la variante como primer argumento y el diccionario como segundo
    python tests_aleatorios.py "%VARIANTE_IN%" "%DICCIONARIO%"
    goto :fin
)

:: SI HAY ARCHIVO DE TEXTO -> EJECUCION NORMAL
if not exist "%ARCHIVO_TEXTO%" (echo Error: no existe %ARCHIVO_TEXTO% & exit /b 1)

set /p TEXTO_INDIV= < "%ARCHIVO_TEXTO%"
echo Ejecutando separarPalabras variante %VARIANTE_IN% con %DICCIONARIO%...
python separarPalabras.py "%VARIANTE_IN%" "%DICCIONARIO%" "%TEXTO_INDIV%"

:fin
endlocal
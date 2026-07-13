# Requerimientos del Proyecto

A continuación se detallan las herramientas y dependencias necesarias para poder ejecutar el código de cada una de las actividades. No se requiere la instalación de librerías externas complejas, sino principalmente herramientas de sistema.

## Actividad 2: Lexer para Dockerfile
- **Lenguaje:** Python 3.6 o superior.
- **Librerías:** No requiere librerías externas (solo utiliza los módulos estándar `re` y `sys`).
- **Ejecución:** Simplemente tener Python agregado al PATH del sistema operativo (Windows/Linux/Mac).

## Actividad 3: Lexer para Subconjunto de Rust
Esta actividad utiliza `flex` para generar código en C, por lo que requiere herramientas de compilación de C/C++.
- **Generador Léxico:** `flex` (Fast Lexical Analyzer Generator).
- **Compilador C:** `gcc` (GNU Compiler Collection) o equivalente.
- **En Windows:** Se recomienda instalar [MSYS2](https://www.msys2.org/), [MinGW-w64](https://www.mingw-w64.org/), o utilizar **WSL** (Windows Subsystem for Linux) o Git Bash (si incluye los paquetes de build).
  - *Comando MSYS2/Ubuntu:* `sudo apt install flex gcc`
- **En Linux/Mac:** Instalar mediante los gestores de paquetes `apt`, `yum` o `brew`.

## Actividad 4: Lexer para Reglas de Seguridad (Snort)
- **Lenguaje:** Python 3.6 o superior.
- **Librerías:** No requiere librerías externas (`re` y `sys`).
- **Ejecución:** Simplemente tener Python en el sistema.

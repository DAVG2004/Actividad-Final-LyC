# Actividades de Código - Tema 4: Análisis Léxico

Este repositorio contiene las soluciones a las actividades de código correspondientes a la evaluación del Tema 4 de Lenguaje y Compiladores.

> **Importante:** Para verificar qué programas o versiones necesitas para correr los proyectos, por favor revisa el archivo **[Requerimientos.md](Requerimientos.md)**.

## 📝 Actividad 2: Lexer para Verificación de Archivos Docker

Ubicada en la carpeta `Actividad_2`. Se ha implementado un analizador léxico en Python (`docker_lexer.py`) desde cero. 
El lexer captura las instrucciones principales de un `Dockerfile`. 

Se incluyen 3 escenarios de prueba:
1. `Dockerfile.test1`: Caso feliz estándar con una imagen de Node.
2. `Dockerfile.test2`: Caso complejo con múltiples variables de entorno y comandos multilínea.
3. `Dockerfile.test3`: Caso con un error léxico introducido (`FRM` en lugar de `FROM`), que será capturado como un error e informará la línea y columna exacta.

**Ejecución:**
```bash
cd Actividad_2
python docker_lexer.py Dockerfile.test1
python docker_lexer.py Dockerfile.test2
python docker_lexer.py Dockerfile.test3
```

---

## 🦀 Actividad 3: Lexer para Subconjunto de Rust (Flex)

Ubicada en la carpeta `Actividad_3`. Se ha desarrollado la especificación en Flex (`rust_sub_lexer.l`) para un subconjunto del lenguaje Rust. 
El subconjunto soporta:
- Palabras clave: `fn`, `let`, `mut`, `if`, `else`, `return`
- Tipos primitivos y booleanos.
- Identificadores, números y operadores principales.
- Ignora espacios, tabuladores y comentarios `//`.

Se incluye el archivo de prueba `test.rs`.

**Compilación y Ejecución:**
```bash
cd Actividad_3
flex rust_sub_lexer.l
gcc lex.yy.c -o rust_lexer
./rust_lexer test.rs
```

---

## 🔒 Actividad 4: Aplicación en Seguridad Informática

Ubicada en la carpeta `Actividad_4`. Se propone una solución (`snort_lexer.py`) para analizar léxicamente reglas tipo **Snort** / **YARA**.
Esta implementación en Python utiliza expresiones regulares para capturar:
- `ACCION` (alert, drop, etc.)
- `PROTOCOLO` (tcp, udp, icmp)
- `DIRECCION_IP`
- `PUERTO`
- `DIRECCIONALIDAD` (`->`, `<>`)
- `OPCION_REGLA` (msg, content, sid, rev)

**Ejecución:**
```bash
cd Actividad_4
python snort_lexer.py
```
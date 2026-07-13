# Guía de Desarrollo Práctico - Tema 4: Análisis Léxico
## Asignatura: Lenguaje y Compiladores (UNEG 2026-I)

Esta documentación técnica sirve como especificación de diseño e ingeniería para el desarrollo rápido de las actividades de código exigidas en la evaluación del Tema 4.

---

## 📅 Resumen del Plan de Entrega (Checklist Rápido)
- [ ] **Actividad 2:** Código Python (`docker_lexer.py`) + 3 Dockerfiles de prueba.
- [ ] **Actividad 3:** Especificación Flex (`rust_sub_lexer.l`) + Código C generado (`lex.yy.c`) + Binario compilado + Repositorio Git con este `README.md`.
- [ ] **Actividad 4:** Archivo de definición léxica para reglas de Seguridad (ej. Snort/YARA).

---

## 🐳 Actividad 2: Lexer para Verificación de Archivos Docker (Desde Cero en Python)

### 1. Requerimientos de Tokenización
El analizador léxico debe reconocer las instrucciones principales de un `Dockerfile` mediante expresiones regulares estrictas utilizando anclas de inicio de línea (`^`) debido a la naturaleza imperativa del formato de Docker.

### 2. Estructura de Tokens a Implementar
*   `FROM`: `r'^FROM'`
*   `RUN`: `r'^RUN'`
*   `ENV`: `r'^ENV'`
*   `COPY`: `r'^COPY'`
*   `WORKDIR`: `r'^WORKDIR'`
*   `CMD`: `r'^CMD'`
*   `EXPOSE`: `r'^EXPOSE'`
*   `ARG_VALUE`: `r'[^\s#]+'` (Cadenas, rutas, imágenes o argumentos)
*   `COMMENT`: `r'#.*'` (Líneas de comentarios)
*   `NEWLINE`: `r'
'`
*   `SKIP`: `r'[ 	]+'`

### 3. Código Base de Implementación Rápida (`docker_lexer.py`)
```python
import re
import sys

tokens = [
    ('FROM', r'^FROM'),
    ('RUN', r'^RUN'),
    ('ENV', r'^ENV'),
    ('COPY', r'^COPY'),
    ('WORKDIR', r'^WORKDIR'),
    ('CMD', r'^CMD'),
    ('EXPOSE', r'^EXPOSE'),
    ('COMMENT', r'#.*'),
    ('NEWLINE', r'
'),
    ('SKIP', r'[ 	]+'),
    ('ARG_VALUE', r'[^\s#]+'),
    ('MISMATCH', r'.')
]

def tokenize(code):
    # Compilar con MULTILINE para que ^ funcione al inicio de cada línea
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    line_num = 1
    line_start = 0
    
    for mo in re.finditer(token_regex, code, re.MULTILINE):
        kind = mo.lastgroup
        value = mo.group(kind)
        column = mo.start() - line_start
        
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind in ('SKIP', 'COMMENT'):
            continue
        elif kind == 'MISMATCH':
            print(f"[❌ ERROR LÉXICO] Carácter inesperado '{value}' en la línea {line_num}, columna {column}")
            sys.exit(1)
        
        yield kind, value, line_num, column

# Plantilla de ejecución para las 3 pruebas requeridas
if __name__ == '__main__':
    sample_dockerfile = """# Prueba 1: Base de Node
FROM node:18-alpine
WORKDIR /app
ENV PORT=3000
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]"""
    
    print("=== Ejecutando Análisis Léxico en Dockerfile ===")
    for token in tokenize(sample_dockerfile):
        print(f"Línea {token[2]} | Token: {token[0]:<10} | Lexema: {token[1]}")
```

### 4. Casos de Prueba Obligatorios (Diseñar 3 escenarios)
1.  **Caso Feliz (Standard):** Un `Dockerfile` clásico de Node.js o Python sin errores.
2.  **Caso Complejo:** Uso exhaustivo de variables de entorno (`ENV`), argumentos (`ARG`), y comentarios interlineados.
3.  **Caso de Error Léxico:** Introducir caracteres inválidos o romper palabras clave (ej. `FRM` en lugar de `FROM`), validando que el token `MISMATCH` actúe capturando el error e informando la línea exacta.

---

## 🦀 Actividad 3: Lexer para Subconjunto de Rust (Con Metacompilador Flex)

### 1. Definición del Lenguaje Reducido $L \subset 	ext{Rust}$
Para mantener el desarrollo ágil y acotado, el subconjunto $L$ soportará:
*   **Palabras reservadas:** `fn`, `let`, `mut`, `if`, `else`, `return`, `true`, `false`.
*   **Tipos primitivos:** `i32`, `f32`, `bool`.
*   **Identificadores:** `[a-zA-Z_][a-zA-Z0-9_]*`
*   **Operadores:** `=`, `==`, `+`, `-`, `*`, `/`, `->`, `;`, `,`, `:`, `::`.
*   **Bloques:** Delimitadores `{`, `}`, `(`, `)`.

### 2. Estructura del Archivo de Especificación Flex (`rust_sub_lexer.l`)
```c
%{
#include <stdio.h>
%}

%option noyywrap

%%

"fn"        { printf("TOKEN: TK_FN, Lexema: %s\n", yytext); }
"let"       { printf("TOKEN: TK_LET, Lexema: %s\n", yytext); }
"mut"       { printf("TOKEN: TK_MUT, Lexema: %s\n", yytext); }
"if"        { printf("TOKEN: TK_IF, Lexema: %s\n", yytext); }
"else"      { printf("TOKEN: TK_ELSE, Lexema: %s\n", yytext); }
"return"    { printf("TOKEN: TK_RETURN, Lexema: %s\n", yytext); }
"i32"       { printf("TOKEN: TK_TYPE_I32, Lexema: %s\n", yytext); }
"bool"      { printf("TOKEN: TK_TYPE_BOOL, Lexema: %s\n", yytext); }

[0-9]+      { printf("TOKEN: TK_NUM_INT, Lexema: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]* { printf("TOKEN: TK_IDENTIFIER, Lexema: %s\n", yytext); }

"=="        { printf("TOKEN: TK_OP_EQ, Lexema: %s\n", yytext); }
"="         { printf("TOKEN: TK_ASSIGN, Lexema: %s\n", yytext); }
"+"         { printf("TOKEN: TK_PLUS, Lexema: %s\n", yytext); }
"->"        { printf("TOKEN: TK_ARROW, Lexema: %s\n", yytext); }
";"         { printf("TOKEN: TK_SEMICOLON, Lexema: %s\n", yytext); }
":"         { printf("TOKEN: TK_COLON, Lexema: %s\n", yytext); }

"//".*      { /* Ignorar comentarios de una línea */ }
[ \t\n]+   { /* Ignorar espacios en blanco, tabuladores y saltos de línea */ }

.           { printf("[❌ ERROR LÉXICO] Carácter no válido: %s\n", yytext); }

%%

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror("Error al abrir el archivo de prueba");
            return 1;
        }
        yyin = file;
    }
    yylex();
    return 0;
}
```

### 3. Pipeline de Compilación en Linux (Comandos para terminal)
```bash
# 1. Generar el código fuente en C a partir del archivo .l
flex rust_sub_lexer.l

# 2. Compilar el archivo de C generado automáticamente junto con GCC
gcc lex.yy.c -o rust_lexer

# 3. Crear un archivo de prueba en el subconjunto de Rust (test.rs)
echo "fn main() { let mut x: i32 = 42; }" > test.rs

# 4. Ejecutar el analizador léxico pasando el archivo de prueba
./rust_lexer test.rs
```

---

## 🔒 Actividad 4: Aplicación en Seguridad Informática (Estrategia)

### 1. Lenguaje Seleccionado: Reglas de Snort / Reglas YARA
Se trabajará sobre el diseño de un lexer para **Reglas de Snort** (Sistema de Detección de Intrusos) o **YARA** (Identificación de Malware), ya que ambos utilizan una estructura basada en expresiones regulares y patrones fijos para la detección de amenazas.

### 2. Propuesta de Tokenización Esencial (Modelo Snort)
*   `ACCION`: `r'(alert|log|pass|drop|reject)'`
*   `PROTOCOLO`: `r'(tcp|udp|icmp|ip)'`
*   `DIRECCION_IP`: `r'([0-9]{1,3}\.){3}[0-9]{1,3}|any'`
*   `DIRECCIONALIDAD`: `r'->|<>'`
*   `OPCION_REGLA`: `r'msg|content|sid|rev|classtype'`

*Esta estructuración teórica-práctica resuelve los requerimientos de código solicitados de manera limpia y modular.*

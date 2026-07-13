import re
import sys

tokens = [
    ('FROM', r'^FROM '),
    ('RUN', r'^RUN '),
    ('ENV', r'^ENV '),
    ('COPY', r'^COPY '),
    ('WORKDIR', r'^WORKDIR '),
    ('CMD', r'^CMD '),
    ('EXPOSE', r'^EXPOSE '),
    ('COMMENT', r'#.*'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH_KEYWORD', r'^[A-Z]+ '), # Captures invalid keywords at the start of a line
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
        elif kind in ('MISMATCH', 'MISMATCH_KEYWORD'):
            print(f"[❌ ERROR LÉXICO] Carácter o instrucción inesperada '{value.strip()}' en la línea {line_num}, columna {column}")
            sys.exit(1)
        
        yield kind, value, line_num, column

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"=== Ejecutando Análisis Léxico en {sys.argv[1]} ===")
        for token in tokenize(code):
            print(f"Línea {token[2]} | Token: {token[0]:<10} | Lexema: {token[1]}")
    else:
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

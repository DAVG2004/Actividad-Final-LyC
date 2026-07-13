import re
import sys

# Definición de tokens para reglas de Snort simplificadas
tokens = [
    ('ACCION', r'\b(alert|log|pass|drop|reject)\b'),
    ('PROTOCOLO', r'\b(tcp|udp|icmp|ip)\b'),
    ('DIRECCION_IP', r'\b(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}|any)\b'),
    ('PUERTO', r'\b[0-9]+\b|any'),
    ('DIRECCIONALIDAD', r'->|<>'),
    ('OPCION_REGLA', r'\b(msg|content|sid|rev|classtype)\b'),
    ('CADENA', r'"[^"]*"'),
    ('ASIGNACION', r':'),
    ('PUNTO_COMA', r';'),
    ('PARENTESIS_ABRIR', r'\('),
    ('PARENTESIS_CERRAR', r'\)'),
    ('ESPACIO', r'[ \t\n]+'),
    ('MISMATCH', r'.')
]

def tokenize(code):
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in tokens)
    line_num = 1
    line_start = 0
    
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        column = mo.start() - line_start
        
        if kind == 'ESPACIO':
            if '\n' in value:
                line_start = mo.end()
                line_num += value.count('\n')
            continue
        elif kind == 'MISMATCH':
            print(f"[❌ ERROR LÉXICO] Carácter inesperado '{value}' en la línea {line_num}, columna {column}")
            sys.exit(1)
            
        yield kind, value, line_num, column

if __name__ == '__main__':
    sample_rule = 'alert tcp any any -> 192.168.1.1 80 (msg:"Ataque detectado"; sid:1000001; rev:1;)'
    
    print("=== Ejecutando Análisis Léxico de Regla Snort ===")
    print(f"Regla: {sample_rule}\n")
    for token in tokenize(sample_rule):
        print(f"Línea {token[2]} | Token: {token[0]:<20} | Lexema: {token[1]}")

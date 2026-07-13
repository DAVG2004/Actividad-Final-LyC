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

#ifndef LUMALANG_TOKEN_H_
#define LUMALANG_TOKEN_H_

#pragma once

#include <stdlib.h>
#include <stdint.h>

typedef struct Token
{
    enum
    {
        TOKEN_ARROW,
        TOKEN_EQUALS,
        TOKEN_SEMI,
        TOKEN_LPAREN,
        TOKEN_RPAREN,
        TOKEN_LBRACE,
        TOKEN_RBRACE,
        TOKEN_COMMA,
        TOKEN_PLUS,
        TOKEN_MINUS,
        TOKEN_ASTR,
        TOKEN_DIVIDER,
        TOKEN_MODULO,
        TOKEN_LESS_THAN,
        TOKEN_GREATER_THAN,
        TOKEN_EOF
    } type;

    char *value;
} token_t;

token_t *init_token(char *value, int32_t type);
void free_token(token *token);

#endif
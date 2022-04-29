#ifndef LUMALANG_TOKEN_H_
#define LUMALANG_TOKEN_H_

#pragma once

#include <stdlib.h>

typedef struct TOKEN_STRUCT
{
    enum
    {
        TOKEN_ARROW
    } type;

    char *value;
} token_t;

token_t *init_token(char *value, int type);
void free_token(token *token);

#endif
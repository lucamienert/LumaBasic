#ifndef LUMALANG_PARSER_H_
#define LUMALANG_PARSER_H_

#pragma once

#include <stdio.h>
#include <stdlib.h>

#include "token.h"
#include "tokenizer.h"
#include "ast.h"

typedef struct Parser
{
    tokenizer_t *tokenizer;
    token_t *token;
} parser_t;

parser_t *init_parser(tokenizer_t *tokenizer);

token_t *eat(parser_t *parser, int type);



#endif
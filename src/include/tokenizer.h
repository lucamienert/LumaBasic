#ifndef LUMALANG_TOKENIZER_H_
#define LUMALANG_TOKENIZER_H_

#pragma once

#include <stdlib.h>
#include <stdint.h>

typedef struct Tokenizer
{
    char *source;
    uint32_t index; 
    char current;
} tokenizer_t;

tokenizer_t *init_tokenizer(char *source);

char peek(tokenizer_t *tokenizer, int32_t offset)
char *get_char_as_string(tokenizer_t *tokenizer);

void next_character(tokenizer_t *tokenizer);
void skip_whitespace(tokenizer_t *tokenizer);
void skip_comment(tokenizer_t *tokenizer);

token_t *move_with_token(tokenizer_t *tokenizer, token_t *token);
token_t *get_next_token(tokenizer_t *tokenizer);

void free_tokenizer(tokenizer_t *tokenizer);

#endif
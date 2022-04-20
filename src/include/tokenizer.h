#ifndef LUMALANG_TOKENIZER_H_
#define LUMALANG_TOKENIZER_H_

#pragma once

typedef struct TOKENIZER_STRUCT
{
    char *source;
    unsigned int index; 
    char current;
} tokenizer_t;

tokenizer_t *init_tokenizer(char *source);

#endif
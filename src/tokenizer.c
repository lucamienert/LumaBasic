#include "include/tokenizer.h"

tokenizer_t *init_tokenizer(char *source)
{
    tokenizer_t *tokenizer = malloc(sizeof(struct TOKENIZER_STRUCT));
    tokenizer->source = source;
    tokenizer->index = 0;
    tokenizer->current = tokenizer->source[tokenizer->index];
    return tokenizer;
}
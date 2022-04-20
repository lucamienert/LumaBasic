#include "include/token.h"

token_t *init_token(char *value, int type)
{
    token_t *token = malloc(sizeof(struct TOKEN_STRUCT));
    token->type = type;
    token->value = value;
    return token;
}
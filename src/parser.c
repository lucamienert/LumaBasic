#include "include/parser.h"

parser_t *init_parser(tokenizer_t *tokenizer)
{
    parser_t *parser = malloc(sizeof(struct Parser));
    parser->tokenizer = tokenizer;
    parser->token = get_next_token(tokenizer);
    return parser;
}

token_t *eat(parser_t *parser, int type)
{
    if (parser->token->type != type)
        exit(1);

    parser->token = get_next_token(parser->tokenizer);
    return parser->token;
}
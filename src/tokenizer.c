#include "include/tokenizer.h"

tokenizer_t *init_tokenizer(char *source)
{
    tokenizer_t *tokenizer = malloc(sizeof(struct TOKENIZER_STRUCT));
    tokenizer->source = source;
    tokenizer->index = 0;
    tokenizer->current = tokenizer->source[tokenizer->index];
    return tokenizer;
}

void next_character(tokenizer_t *tokenizer)
{
    if(tokenizer->current == '\0' && tokenizer->index > strlen(tokenizer->source))
        return;

    tokenizer->index++;
    tokenizer->current = tokenizer->source[tokenizer->index];
}

char peek(tokenizer_t *tokenizer, int offset)
{
    return tokenizer->source[tokenizer->index + offset];
}

void skip_whitespace(tokenizer_t *tokenizer)
{
    while(tokenizer->current == ' ' || tokenizer->current == 10 || tokenizer->current == 13 || tokenizer->current == '\t')
        next_character(tokenizer);
}

void skip_comment(tokenizer_t *tokenizer)
{
    if(tokenizer->current == '#' && peek(tokenizer->current, 1) == '#')
    {
        while(tokenizer->current != '\n')
            next_character(tokenizer);
    }

    skip_whitespace(tokenizer);
}

token_t *move_with_token(tokenizer_t *tokenizer, token_t *token)
{
    next_character(tokenizer);
    return token;
}

char *get_char_as_string(tokenizer_t *tokenizer)
{
    char *str = calloc(2, sizeof(char));
    str[0] = tokenizer->current;
    str[1] = '\0';

    return str;
}

token_t *get_next_token(tokenizer_t *tokenizer)
{
    while(tokenizer->current != '\0' && tokenizer->index < strlen(tokenizer->source))
    {
        skip_whitespace(tokenizer);
        skip_comment(tokenizer);

        switch(tokenizer->current)
        {
            case '=':
            {
                if(peek(tokenizer, 1) == '>')
                    return move_with_token(tokenizer, init_token("=>", TOKEN_ARROW));

                return move_with_token(tokenizer, init_token("=", TOKEN_EQUALS));
            } break;
            case ';': return move_with_token(tokenizer, init_token(";", TOKEN_SEMI); break;
            case '(': return move_with_token(tokenizer, init_token("(", TOKEN_LPAREN); break;
            case ')': return move_with_token(tokenizer, init_token(")", TOKEN_RPAREN); break;
            case '{': return move_with_token(tokenizer, init_token("{", TOKEN_LBRACE); break;
            case '}': return move_with_token(tokenizer, init_token("}", TOKEN_RBRACE); break;
            case ',': return move_with_token(tokenizer, init_token(",", TOKEN_COMMA); break;
            case '+': return move_with_token(tokenizer, init_token("+", TOKEN_PLUS); break;
            case '-': return move_with_token(tokenizer, init_token("-", TOKEN_MINUS); break;
            case '*': return move_with_token(tokenizer, init_token("*", TOKEN_ASTR); break;
            case '/': return move_with_token(tokenizer, init_token("/", TOKEN_DIVIDER); break;
            case '%': return move_with_token(tokenizer, init_token("%", TOKEN_MODULO); break;
            case '<': return move_with_token(tokenizer, init_token("<", TOKEN_LESS_THAN); break;
            case '>': return move_with_token(tokenizer, init_token(">", TOKEN_GREATER_THAN); break;
            default: break;
        }
    }
}

void free_tokenizer(tokenizer_t *tokenizer)
{
    free(tokenizer->source);
    free(tokenizer);
}
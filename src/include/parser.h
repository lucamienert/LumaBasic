#ifndef LUMALANG_PARSER_H_
#define LUMALANG_PARSER_H_

#pragma once

#include <stdlib.h>
#include <stdint.h>

#include "tokenizer.h"
#include "ast.h"
#include "scope.h"

typedef struct Parser
{
    tokenizer_t *tokenizer;
    token_t *current_token;
    token_t *previous_token;
    scope_t *scope;
} parser_t;

parser_t *new_parser(tokenizer_t *tokenizer);

void eat(parser_t *parser, int32_t token_type);

ast_t *parse(parser_t *parser, scope_t *scope);
ast_t *parse_statement(parser_t *parser, scope_t *scope);
ast_t *parse_statements(parser_t *parser, scope_t *scope);
ast_t *parse_expression(parser_t *parser, scope_t *scope);
ast_t *parse_factor(parser_t *parser, scope_t *scope);
ast_t *parse_term(parser_t *parser, scope_t *scope);
ast_t *parse_function_call(parser_t *parser, scope_t *scope);
ast_t *parse_variable_definition(parser_t *parser, scope_t *scope);
ast_t *parse_function_definition(parser_t *parser, scope_t *scope);
ast_t *parse_variable(parser_t *parser, scope_t *scope);
ast_t *parse_string(parser_t *parser, scope_t *scope);
ast_t *parse_id(parser_t *parser, scope_t *scope);

#endif
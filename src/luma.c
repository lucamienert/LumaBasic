#include <stdlib.h>

#include "include/ast.h"
#include "include/io.h"
#include "include/tokenizer.h"
#include "include/visitor.h"
#include "include/parser.h"
#include "include/scope.h"

int main(int argc, char **argv)
{
    if(argc < 2)
        exit(0);

	tokenizer_t *tokenizer = init_tokenizer(get_file(argv[1]));
    parser_t *parser = new_parser(tokenizer);
    ast_t *root_node = parse(parser, parser->scope);
    visitor_t *visitor = new_visitor();
    visit(visitor, root_node);

    return 0;
}
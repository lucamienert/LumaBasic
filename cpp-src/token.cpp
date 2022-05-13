#include "include/token.h"

Token::Token(int type, std::string value)
{
	this->type = type;
	this->value = value;
}

std::string Token::get_value()
{
	switch (type)
	{
	case TOKEN_IDENTIFIER: return "IDENT: " + value; break;
	case TOKEN_KEYWORD: return "KEYWORD: " + value; break;
	case TOKEN_LPAREN: return "LPAREN: " + value; break;
	case TOKEN_RPAREN: return "RPAREN: " + value; break;
	case TOKEN_NUMBER: return "NUMBER: " + value; break;
	case TOKEN_STRING: return "STRING: " + value; break;
	}

	return value;
}

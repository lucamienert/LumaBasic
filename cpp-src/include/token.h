#ifndef token_h_
#define token_h_

#pragma once

#include <string>
#include <vector>

enum
{
	TOKEN_NUMBER,
	TOKEN_STRING,
	TOKEN_IDENTIFIER,
	TOKEN_KEYWORD,
	TOKEN_LPAREN,
	TOKEN_RPAREN,
	TOKEN_EOF
};

class Token
{
private:
	int type;
	std::string value;
public:
	Token(int type, std::string value);
	std::string get_value();
};

#endif
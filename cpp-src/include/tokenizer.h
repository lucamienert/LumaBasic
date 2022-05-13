#pragma once

#include <string>
#include <vector>
#include <ctype.h>

#include "token.h"

class Tokenizer
{
private:
	std::string source;
	char current_char;
	int pos;
public:
	Tokenizer(std::string source);
	void advance();
	std::vector<Token*> make_tokens();
	Token *make_number();
	Token *make_string();
	Token *make_identifier();
	void skip_comment();
	void skip_whitespace();
};
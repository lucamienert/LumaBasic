#include "include/tokenizer.h"

Tokenizer::Tokenizer(std::string source)
{
	this->source = source;
	this->pos = 0;
	this->current_char = this->source[this->pos];
}

void Tokenizer::advance()
{
	if (current_char == '\0')
		return;

	++pos;
	current_char = source[pos];
}

std::vector<Token*> Tokenizer::make_tokens()
{
	std::vector<Token*> tokens{};

	while (current_char != '\0')
	{
		skip_whitespace();
		
		if (isalpha(current_char))
			tokens.push_back(make_identifier());
		
		if (isdigit(current_char))
			tokens.push_back(make_number());

		if (current_char == '"')
			tokens.push_back(make_string());

		switch (current_char)
		{
			case '(': tokens.push_back(new Token(TOKEN_LPAREN, "(")); break;
			case ')': tokens.push_back(new Token(TOKEN_RPAREN, ")")); break;
			default: break;
		}

		advance();
	}

	tokens.push_back(new Token(TOKEN_EOF, "\0"));
	return tokens;
}

Token *Tokenizer::make_number()
{
	std::string s;
	while (isdigit(current_char))
	{
		s.push_back(current_char);
		advance();
	}

	return new Token(TOKEN_NUMBER, s);
}

Token *Tokenizer::make_string()
{
	std::string s;
	advance();
	while (current_char != '"')
	{
		s.push_back(current_char);
		advance();
	}

	advance();
	return new Token(TOKEN_STRING, s);
}

Token *Tokenizer::make_identifier()
{
	std::vector<std::string> keys =
	{
		"end",
		"def",
		"var",
		"to",
		"then",
		"and",
		"or",
		"for",
		"not",
		"if",
		"else",
		"elseif",
		"step",
		"while",
		"return",
		"continue",
		"break"
	};

	std::string s;
	while (isalpha(current_char))
	{
		s.push_back(current_char);
		advance();
	}

	for (auto& item : keys)
	{
		if (s == item)
			return new Token(TOKEN_KEYWORD, s);
	}

	return new Token(TOKEN_IDENTIFIER, s);
}

void Tokenizer::skip_comment()
{
	if (current_char == '#')
	{
		while (current_char != '\n')
			advance();
	}

	skip_whitespace();
}

void Tokenizer::skip_whitespace()
{
	while (current_char == ' ' || current_char == 10 || current_char == 13 || current_char == '\t')
		advance();
}

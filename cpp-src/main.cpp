#include "include/tokenizer.h"
#include <iostream>


int main(int argc, char** argv)
{
	Tokenizer t("for i = 0 to 10 then sysout(\"Test\") end");
	for (auto token : t.make_tokens())
		std::cout << token->get_value() << "\n";

	return 0;
}
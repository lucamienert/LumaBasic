#include "include/io.h"

char *get_file(char *filename)
{
    char *buffer = 0;
    size_t length;

    FILE *file = fopen(filename, "rb");
    if(!file)
        exit(2);

    fseek(file, 0, SEEK_END);
    length = ftell(file);
    fseek(file, 0, SEEK_SET);
    buffer = calloc(length, length);

    if(buffer)
        fread(buffer, 1, length, file);

    fclose(file);
    return buffer;
}
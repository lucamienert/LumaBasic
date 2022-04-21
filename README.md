# LUMA Language

## Description

An toy programming language for my operating system.
For now it is using the C-Standard Libary but I will change it to my
custom C-Libary, specialized for LumaOS. It is still an very early work in progress so building it will do nothing but throw errors.

Features to implement (or already implemented):

- [ ] Lexical analysis

## Usage

### Prerequisites

- nasm (for later compiling)
- gcc

### Building

```bash
make
```

### Using

```bash
./bin/lumalang.out <your .luma file>
```

Alternatively you can program your program into an C-String and compile it yourself.

## Resources

- [Writing an C Compiler](https://norasandler.com/2017/11/29/Write-a-Compiler.html)
- [How to write a very basic compiler](https://softwareengineering.stackexchange.com/questions/165543/how-to-write-a-very-basic-compiler)
- [TAC](https://github.com/sebbekarlsson/tac)
- [Hermes](https://github.com/sebbekarlsson/hermes)
- [Youtube](https://www.youtube.com/watch?v=WABO4o_y8qc)
- [Compiler](https://de.wikipedia.org/wiki/Compilerbau)

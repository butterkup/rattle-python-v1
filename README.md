# Rattle <sub><sub>😵</sub></sub>

__rattle__ is a small compiled programming language with a mix of static and dynamic features spread through, for sample source code see [src/](src/).

> Note: Rattle source files have the `.rat` extension.

## Introduction

Project *rattle* is an attempt at compiler design. Compiler being a two phased process to excuting a source program; the compilation to bytecode and the executon of the bytecode in a virtual machine. Along the way, we'll add optimizations to the bytecode, learn about dynamic algorithms and the mysterious symbol table.

## Knows

The project is entirely written in python with the aim being to reduce low level complexity that using languages like C/C++/Rust would introduce. Speed is not the main goal as the project will involve many aspects to be considered.

The most exciting part of this is optimization, unfortunately we'll not be using actual machine instrution rather a simple well defined set that we'll create ourselves to run in a small virtual machine, the good news is, like machine instructions, bytecode can be optimized really well, unfortuanately achieving the speed of machine code is almost impossible but this will not stop us from reaching our goal.

## Mentions

Most content in this project is self researched and may not be the best in practice.

Some resources are worth mentioning though; the book `Compiler principles, techniques and tools` by `Alfre Aho` and `Crafting Interpreters` by `Robert Nystrom` are amazing reads on this topic.

## RoadMap

First, we lex a string to produce tokens and report any invalid characters found, then we parse the token stream to an abstract syntax tree `AST` which we will use to do some partial optimizations like constant folding in the expression tree, we can also expand loops if we know how many iterations it will run, and also semantic analysis; check if `break`, `continue` and `return` have been used in their expected scopes and also resolve variables. After this we compile the AST as we did in [YAP project](http://github.com/thee-dushbag/yap.git) exprlang. All optimizations in the AST will be done using visitors; ie `ExpressionVisitor` and `StatementVisitor`.

This is not the best way but a good place to start. Further optimizations will be enforced in bytecode.

# cpy Language Compiler ⚙️🐍

[cite_start]A complete, full-cycle compiler written in **Python** that translates source code from a custom programming language called **`cpy`** into optimized, low-level **Assembly (.asm)**[cite: 270, 271, 443, 458]. This project simulates all the core stages of modern compiler construction, built entirely from scratch without using automated parsing tools (like Lex/Yacc or ANTLR).

---

## 🚀 Architectural Pipeline & Components

[cite_start]The compiler processes the source `.cpy` file sequentially through the following distinct compilation phases[cite: 275, 443]:

### 1. Lexical Analyzer (Lexer / Tokenizer) 📊
* [cite_start]Processes the source file character-by-character to group valid patterns into structural **lexical units (tokens)**[cite: 275].
* [cite_start]Dynamically maps tokens into specific grammatical families: `taken` (reserved language keywords like `#def`, `#int`), `celebrant` (delimiters/brackets), `rel_op` (relational operators), `identifier` (variables), `constant` (literals), `add_op`/`mul_op` (arithmetic), and `comment`[cite: 278, 279, 280, 281].
* [cite_start]Tracks execution safety using a finite state machine (FSM) over line counters to pinpoint precise errors[cite: 282, 283, 284].

### 2. Syntax Analyzer (Parser) 📝
* [cite_start]Utilizes a deterministic **LL / Recursive Descent Parser** architecture to validate the token stream against the context-free grammar constraints of the `cpy` language[cite: 356].
* [cite_start]Rigorously enforces scope management, statement evaluations (`if-elif-else`, `while` loops, function definitions), explicit structures (`defglobal`, `defdef`), and error handling at the exact line number[cite: 358, 360, 361, 380, 381, 382, 383, 403].

### 3. Intermediate Code Generation (ICG) 📉
* [cite_start]Translates the validated syntax tree into **3-Address Code** serialized as a linear stream of **Quadruples (Quads)**[cite: 407, 408].
* [cite_start]Each quad tracks execution steps formatted as: `[label, operator, operand1, operand2, operand3]`[cite: 408].
* [cite_start]Implements foundational optimization and execution functions like `genQuad`, `nextQuad`, `newTemp` (for temporary variable creation), and a dynamic `backpatch` mechanism to resolve forward jumps and logical routing inside branches/loops[cite: 407, 410, 412, 413, 414].
* [cite_start]Emits the intermediate state architecture into a compiled `endiamesos.int` log file[cite: 415].

### 4. Symbol Table Management 🧬
* [cite_start]Manages nested lexical scopes via a dynamic multi-level stack (`createScope`, `deleteScope`) to enforce proper variable encapsulation and separate global variables from local runtime definitions[cite: 427, 429, 441].
* [cite_start]Tracks specific `entities` across dynamic memory stack frame tracking (`updateOffset`, `findLastOffset`)[cite: 427, 434].
* [cite_start]Exports a deep-copy evolutionary timeline of variable scopes directly into a `symbol.sym` output ledger[cite: 435, 436].

### 5. Final Assembly Code Generation (Target Language) 💻
* [cite_start]Parses the generated quadruples stream and mappings to systematically translate variables into cross-platform **Assembly** syntax[cite: 443].
* [cite_start]Implements low-level compiler abstractions like `loadvr` and `storerv` to emit optimized load/store (`lw`/`sw`) assembly routines[cite: 447, 448].
* [cite_start]Automatically orchestrates register memory allocation by resolving lookups from the global data pointer (`$gp`) or the stack activation pointer (`$sp`)[cite: 450].
* [cite_start]Emits a fully executable target file named `final.asm`[cite: 458].

---

## 📂 Expected Output Files

Upon running a successful compilation against a `.cpy` script, the engine generates three standard logs:
1. [cite_start]**`endiamesos.int`** – Linear transcript containing all the compiled three-address quads[cite: 415].
2. [cite_start]**`symbol.sym`** – Step-by-step state snapshot of the Symbol Table across all nesting levels[cite: 435, 436].
3. [cite_start]**`final.asm`** – The final generated target assembly file[cite: 458].

---

## ⚙️ Execution

To compile a `.cpy` program file, execute the master script through your Python terminal terminal:

```bash
python main.py --input test_program.cpy

# cpy Language Compiler ⚙️🐍

A complete, full-cycle compiler written in **Python** that translates source code from a custom programming language called **`cpy`** into optimized, low-level **Assembly (.asm)**. This project simulates all the core stages of modern compiler construction, built entirely from scratch without using automated parsing tools (like Lex/Yacc or ANTLR).

---

## 🚀 Architectural Pipeline & Components

The compiler processes the source `.cpy` file sequentially through the following distinct compilation phases:

### 1. Lexical Analyzer (Lexer / Tokenizer) 📊
* Processes the source file character-by-character to group valid patterns into structural **lexical units (tokens)**.
* Dynamically maps tokens into specific grammatical families: `taken` (reserved language keywords like `#def`, `#int`), `celebrant` (delimiters/brackets), `rel_op` (relational operators), `identifier` (variables), `constant` (literals), `add_op`/`mul_op` (arithmetic), and `comment`.
* Tracks execution safety using a finite state machine (FSM) over line counters to pinpoint precise errors.

### 2. Syntax Analyzer (Parser) 📝
* Utilizes a deterministic **LL / Recursive Descent Parser** architecture to validate the token stream against the context-free grammar constraints of the `cpy` language.
* Rigorously enforces scope management, statement evaluations (`if-elif-else`, `while` loops, function definitions), explicit structures (`defglobal`, `defdef`), and error handling at the exact line number.

### 3. Intermediate Code Generation (ICG) 📉
* Translates the validated syntax tree into **3-Address Code** serialized as a linear stream of **Quadruples (Quads)**.
* Each quad tracks execution steps formatted as: `[label, operator, operand1, operand2, operand3]`.
* Implements foundational optimization and execution functions like `genQuad`, `nextQuad`, `newTemp` (for temporary variable creation), and a dynamic `backpatch` mechanism to resolve forward jumps and logical routing inside branches/loops.
* Emits the intermediate state architecture into a compiled `endiamesos.int` log file.

### 4. Symbol Table Management 🧬
* Manages nested lexical scopes via a dynamic multi-level stack (`createScope`, `deleteScope`) to enforce proper variable encapsulation and separate global variables from local runtime definitions.
* Tracks specific `entities` across dynamic memory stack frame tracking (`updateOffset`, `findLastOffset`).
* Exports a deep-copy evolutionary timeline of variable scopes directly into a `symbol.sym` output ledger.

### 5. Final Assembly Code Generation (Target Language) 💻
* Parses the generated quadruples stream and mappings to systematically translate variables into cross-platform **Assembly** syntax.
* Implements low-level compiler abstractions like `loadvr` and `storerv` to emit optimized load/store (`lw`/`sw`) assembly routines.
* Automatically orchestrates register memory allocation by resolving lookups from the global data pointer (`$gp`) or the stack activation pointer (`$sp`).
* Emits a fully executable target file named `final.asm`.

---

## 📂 Expected Output Files

Upon running a successful compilation against a `.cpy` script, the engine generates three standard logs:
1. **`endiamesos.int`** – Linear transcript containing all the compiled three-address quads.
2. **`symbol.sym`** – Step-by-step state snapshot of the Symbol Table across all nesting levels.
3. **`final.asm`** – The final generated target assembly file.

---

## ⚙️ Execution

To compile a `.cpy` program file, execute the master script through your terminal:

```bash
python main.py --input test_program.cpy

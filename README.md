# Super Stack Assembly Intepreter

A minimal stack based assembly language. Super Stack has similar instructions to the whitespace language and can be used to assemble whitespace programs.

## Hello World

```assembly
.main:
    push 0
    push "Hello World!"
.print:
    copy
    jz .end
    putchar
    jmp .print
.end:
    pop
    halt
```

[examples](#examples)

## Usage

```shell
python3 ss.py filename.asm
```

## Instruction Set

### Stack operations

| Instruction | Meaning                                                       |
| ----------- | ------------------------------------------------------------- |
| PUSH        | Push data onto the stack                                      |
| POP         | Pop data from the stack                                       |
| SWAP        | Swap items at the top of the stack                            |
| COPY        | Copy item from a given stack position to the top of the stack |

```assembly
push 1  # [1]
push 2  # [1, 2]
copy    # [1, 2, 2]
pop     # [1, 2]
copy 1  # [1, 2, 1]
swap    # [1, 1, 2]
halt
```

### Heap operations

| Instruction | Meaning                        |
| ----------- | ------------------------------ |
| STORE       | Store value at memory address  |
| ACCESS      | Access value at memory address |
|             |                                |

```assembly
push 100  # [100]
push 7    # [100, 7]
store     # heap: {100: 7}, stack: []
push 100  # [100]
access    # [7]
halt
```

### Program instructions

| Instruction | Meaning                                                   |
| ----------- | --------------------------------------------------------- |
| JMP         | Jump                                                      |
| JZ          | Jump if item at the top of the stack is zero              |
| JNZ         | Jump if not zero                                          |
| JL          | Jump if less than zero                                    |
| JG          | Jump if greater than zero                                 |
| CALL        | Push program position to the call stack and jump to label |
| RET         | Return to position at the top of the call stack           |
| HALT        | Halt                                                      |

### Arithmetic operations

| Instruction | Meaning  |
| ----------- | -------- |
| ADD         | Add      |
| SUB         | Subtract |
| MUL         | Multiply |
| DIV         | Divide   |

```assembly
push 7  # [7]
push 1  # [7, 1]
sub     # [-6]
halt
```

### IO Instructions

| Instruction | Meaning                                                      |
| ----------- | ------------------------------------------------------------ |
| READ        | Read integer from console (stores in heap)                   |
| PUTS        | Write integer to console                                     |
| READCHAR    | Read character from input (file or console) [stores in heap] |
| PUTCHAR     | Write character to output (file or console)                  |
| OPENF       | Open file                                                    |
| CLOSEF      | Close file                                                   |
| DUMP        | Dump memory                                                  |

```assembly
push 1        # Open file for writting
openf "a.txt"
push 117
putchar       # Write character 'A' to a.txt
closef

push 0        # Open file for reading
openf "a.txt"
push 100
copy          # [100, 100]
readchar      # {100: 117} [100]
closef

access        # [117]
putchar       # A
halt
```

## Examples

[all examples](./examples)

### 99 bottles

```assembly
.main:
    push 100
.loop:
    # Print number of bottles
    copy
    puts

    push 0
    push " bottles of beer on the wall,"
    call .print

    copy
    puts
    push 0
    push 10
    push " bottles of beer"
    call .print

    # Subtract 1 bottle
    copy
    push 1
    swap
    sub

    push 0
    push "Take one down and pass it around"
    call .print

    copy
    puts
    push 0
    push 10
    push 10
    push " bottles of beer on the wall."
    call .print

    # Check for end of loop
    copy
    jz .end
    jmp .loop
.print:
    copy
    putchar
    jnz .print
    ret
.end:
    pop
    halt

```

## Truth machine

```assembly
.main:
    push 63
    putchar
    push 100
    readchar
    push 100
    haccess
.loop:
    copy
    push 48
    sub
    jnz .loop
    halt

```


import sys


class Memory:
    program = []
    stack = []
    heap = {}
    labels = {}
    call_stack = []
    io_buffer = []
    line_number = 0
    io_output = None


# Stack instructions --------------------------

def push(memory: Memory, value: str):
    if value[0] == '"' or value[0] == "'":
        # Handle push "string"
        for i in reversed(range(1, len(value) - 1)):
            memory.stack.append(ord(value[i]))
        return

    memory.stack.append(int(value))


def pop(memory: Memory):
    memory.stack.pop()


def swap(memory: Memory):
    a = memory.stack.pop()
    b = memory.stack.pop()

    memory.stack.append(a)
    memory.stack.append(b)


def copy(memory: Memory, offset_str: str = '0'):
    offset = len(memory.stack) - int(offset_str) - 1
    memory.stack.append(memory.stack[offset])


# Program instructions -----------------------------

def jmp(memory: Memory, label: str):
    if label not in memory.labels:
        error(memory, 'undefined label')
        return

    memory.line_number = memory.labels[label]


def jz(memory: Memory, label: str):
    if memory.stack.pop() == 0:
        jmp(memory, label)


def jnz(memory: Memory, label: str):
    if memory.stack.pop() != 0:
        jmp(memory, label)


def jl(memory: Memory, label: str):
    if memory.stack.pop() < 0:
        jmp(memory, label)


def jg(memory: Memory, label: str):
    if memory.stack.pop() > 0:
        jmp(memory, label)


def call(memory: Memory, label: str):
    memory.call_stack.append(memory.line_number)
    jmp(memory, label)


def ret(memory: Memory):
    if len(memory.call_stack) == 0:
        return

    caller = memory.call_stack.pop()
    memory.line_number = caller


def halt(memory: Memory) -> int:
    return 0


# Heap instructions --------------------------

def store(memory: Memory):
    value = memory.stack.pop()
    address = memory.stack.pop()
    memory.heap[address] = value


def access(memory: Memory):
    address = memory.stack.pop()

    if address not in memory.heap:
        memory.heap[address] = 0

    memory.stack.append(memory.heap[address])


# Arithmetic instructions --------------------

def add(memory: Memory):
    memory.stack.append(memory.stack.pop() + memory.stack.pop())


def sub(memory: Memory):
    memory.stack.append(memory.stack.pop() - memory.stack.pop())


def mul(memory: Memory):
    memory.stack.append(memory.stack.pop() * memory.stack.pop())


def div(memory: Memory):
    memory.stack.append(memory.stack.pop() / memory.stack.pop())


# IO instructions ------------------------------

def read(memory: Memory):
    value = input()
    address = memory.stack.pop()
    memory.heap[address] = int(value)


def puts(memory: Memory):
    if memory.io_output:
        memory.io_output.write(memory.stack.pop(), end='')
        return
    print(memory.stack.pop(), end='')


def readchar(memory: Memory):
    if len(memory.io_buffer) == 0:
        if memory.io_output is not None:
            memory.io_buffer = list(memory.io_output.read())
        else:
            memory.io_buffer = list(input())
            memory.io_buffer.append('\n')

    address = memory.stack.pop()
    memory.heap[address] = ord(memory.io_buffer.pop(0))


def putchar(memory: Memory):
    if memory.io_output:
        memory.io_output.write(chr(memory.stack.pop()))
        return
    print(chr(memory.stack.pop()), end='')


def openf(memory: Memory, file: str):
    if file[0] != '"' or file[-1] != '"':
        error(memory, 'Invalid file name')
        return -1
    modes = {0: 'r', 1: 'w'}
    memory.io_output = open(file[1:-1], modes[memory.stack.pop()])


def closef(memory: Memory):
    memory.io_output.close()
    memory.io_output = None


def dump(memory: Memory):
    out = print

    if memory.io_output:
        out = memory.io_output.writeline

    out(memory.stack)
    out(memory.heap)
    out(memory.call_stack)


def error(memory: Memory, msg: str):
    print('error: %s, line: %d' % (msg, memory.line_number))
    print(memory.stack)
    print(memory.heap)


# --------------------------------------


def parse_labels(memory: Memory):
    for i in range(len(memory.program)):
        line = memory.program[i].strip()

        if '#' in line:
            line = line.split('#')[0]

        memory.program[i] = line

        if line == '':
            continue

        if line[-1] == ':':
            memory.labels[line[:-1]] = i
            continue

ENV = locals()
memory = Memory()


def main(memory: Memory):
    with open(sys.argv[1], 'r') as src:
        memory.program = src.readlines()
        parse_labels(memory)

        while True:
            line = memory.program[memory.line_number].strip()
            memory.line_number += 1

            if line == '':
                continue

            args = line.split(' ')
            instruction = args[0].lower()

            if instruction not in ENV:
                continue

            exit_code = 0

            try:
                if len(args) == 1:
                    exit_code = ENV[instruction](memory)
                else:
                    exit_code = ENV[instruction](memory, ' '.join(args[1:]))
            except Exception as e:
                print(memory.line_number, e)

            if exit_code is not None:
                break

    print()
    print(memory.stack)
    print(memory.heap)


try:
    main(memory)
except KeyboardInterrupt:
    print('bye')

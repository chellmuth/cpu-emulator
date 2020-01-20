import math
from dataclasses import dataclass
from typing import List

from flask import render_template, redirect

import assembler
import instruction_helper
from app import app
from core import Byte, Word, Register, Flag
from emulator import Machine

@dataclass
class DisassembledInstructionView:
    current: bool
    address: str
    hex_str: str
    instruction_text: str

@dataclass
class DisassembledView:
    instructions: List[DisassembledInstructionView]

@dataclass
class RegisterView:
    name: str
    value: str

@dataclass
class StackRowView:
    current: bool
    address: str
    words: List[str]

@dataclass
class StackView:
    columns: int
    rows: List[StackRowView]

@dataclass
class MemoryRowView:
    address: str
    words: List[str]

@dataclass
class MemoryView:
    columns: int
    rows: List[MemoryRowView]

@dataclass
class FlagView:
    name: str
    on: bool

machine = None

def reset_app():
    global machine

    # program = [
    #     "PSH 0x1234568",
    #     "POP rb",
    #     "ADD ra, 0x11223344",
    #     "STR ra, 0x240",
    #     "STB ra, 0x268",
    #     "CAL 0x30",
    #     "POP rd",
    #     "OUT 0x6c000000",
    #     "LOD rc, 0xb",
    #     "LOD rc, ra",
    #     "ADD ra, 0x10000001",
    #     "STB ra, 0x50",
    #     "ADD rb, 0x01000000",
    #     "NOP",
    #     "ORR ra, 0x10010000",
    #     "NOT rc",
    #     "ADD ra, rb",
    #     "ADD ra, 0x30000000",
    #     "RET",
    # ]

    program = [
        "PSH 0x6c",
        "AAL 0x16",
        "POP ra",
        "OUT 0x21",
        "AMP 0x70", # arbitrary end
        "OUT 0x6c",
        "RET"
    ]

    # program = [
    #     "PSH 0x1",
    #     "POP ra",
    #     "XOR ra, 0x3",
    #     "AND ra, rb",
    #     "XOR ra, 0x2",
    #     "NOP",
    # ]

    machine = Machine()

    memory_offset = 0
    for line in program:
        instruction = assembler.parse_to_instruction(line)
        for byte in instruction_helper.get_bytes(instruction):
            machine.memory.write_byte(Word.from_int(memory_offset), byte)
            memory_offset += 1

reset_app()

@app.route('/')
def show():
    return render_emulator()

@app.route('/', methods=["POST"])
def update():
    instruction = machine.next_instruction()
    machine.run(instruction)

    return render_emulator()

@app.route('/reset', methods=["POST"])
def reset():
    reset_app()

    return redirect("/")

def render_emulator():
    instruction = machine.next_instruction()

    if not instruction:
        instruction_view = "--"
    else:
        instruction_view = instruction.human()

    available_actions = set()
    if instruction:
        available_actions.add("step")

    address = 0
    instruction_views = []
    for instruction in machine.glob_instructions(0):
        instruction_views.append(
            DisassembledInstructionView(
                address == machine.registers[Register.pc].int_value(),
                hex(address),
                instruction_helper.bytes_str(instruction),
                instruction.human()
            )
        )
        address += instruction.size

    disassembled_view = DisassembledView(instruction_views)

    registers_view = [
        RegisterView(register.name, machine.registers[register.value].hex_str() )
        for register in Register
    ]

    memory = machine.memory

    columns = 10
    memory_view = MemoryView(columns, [
        MemoryRowView(
            Word.from_int(row * columns * 4).hex_str(),
            [
                memory.read_word((row * columns + column) * 4).hex_str()
                for column in range(columns)
                if (row * columns + column) * 4 < memory.size
            ]
        )
        for row in range(math.ceil(memory.size / (columns * 4)))
    ])

    stack_pointer = machine.registers[Register.sp].int_value()
    stack_view = StackView(1, [
        StackRowView(
            row == 0,
            Word.from_int(stack_pointer + row * 4).hex_str(),
            [
                memory.read_word(stack_pointer + row * 4).hex_str()
            ]
        )
        for row in range(((memory.size - 1) - stack_pointer) // 4)
    ])

    flags_view = [
        FlagView(flag.name, flag.value in machine.flags)
        for flag in Flag
    ]

    stdout_view = "".join([ chr(char.int_value) for char in machine.stdout ])

    return render_template(
        "emulator.html",
        instruction=instruction_view,
        registers=registers_view,
        flags=flags_view,
        disassembled=disassembled_view,
        stack=stack_view,
        memory=memory_view,
        stdout=stdout_view,
        available_actions=available_actions
    )

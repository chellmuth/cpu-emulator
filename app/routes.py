import math
from dataclasses import dataclass
from typing import List

from flask import render_template, redirect

import assembler
import instruction_helper
import orc_parser
from app import app
from core import Byte, Word, Register, Flag
from emulator import Machine

@dataclass
class DisassembledInstructionView:
    current: bool
    address: str
    debug_str: str
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

    machine = Machine()

    orc = orc_parser.parse("chall1.exe")
    segment = orc.segments[1]

    base = segment.base.int_value()
    offset = segment.offset.int_value()

    data = orc.data

    for i in range(segment.size.int_value()):
        machine.memory.write_byte(Word.from_int(base + i), data[offset + i])

    machine.registers[Register.pc] = Word.from_int(base)

reset_app()

@app.route('/')
def show():
    return render_emulator()

@app.route('/', methods=["POST"])
def update():
    instruction = machine.next_instruction()
    machine.run(instruction)

    return render_emulator()

@app.route('/run', methods=["POST"])
def run():
    instruction = machine.next_instruction()
    while instruction:
        machine.run(instruction)
        instruction = machine.next_instruction()

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

    address = machine.registers[Register.pc].int_value() # todo: look backwards
    instruction_views = []
    for instruction in machine.glob_instructions():
        instruction_views.append(
            DisassembledInstructionView(
                address == machine.registers[Register.pc].int_value(),
                Word.from_int(address).hex_str(padded=True),
                instruction.debug_str(),
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

    columns = 1
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

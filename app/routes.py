from dataclasses import dataclass
from typing import List

from flask import render_template, redirect

import assembler
from app import app
from core import Byte, Word, Register
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
class MemoryRowView:
    address: str
    words: List[str]

@dataclass
class MemoryView:
    columns: int
    rows: List[MemoryRowView]


machine = None

def reset_app():
    global machine

    program = [
        "OUT 0x6c000000",
        "LOD rc, 0xb",
        "LOD rc, ra",
        "ADD ra, 0x10000001",
        "AMP 0x1f",
        "STB ra, 0x50",
        "ADD rb, 0x01000000",
        "NOP",
        "JMP 0x6",
        "ORR ra, 0x10010000",
        "NOT rc",
        "ADD ra, rb",
        "ADD ra, 0x30000000",
    ]

    machine = Machine()

    memory_offset = 0
    for line in program:
        instruction = assembler.parse_to_instruction(line)
        for byte in instruction.bytes():
            machine.memory.write(Word.from_int(memory_offset), byte)
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
        print(instruction)
        available_actions.add("step")

    address = 0
    instruction_views = []
    for instruction in machine.glob_instructions(0):
        instruction_views.append(
            DisassembledInstructionView(
                address == machine.registers[Register.pc].int_value(),
                hex(address),
                instruction.bytes_str(),
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
            ]
        )
        for row in range(memory.size // (columns * 4))
    ])

    stdout_view = "".join([ chr(char.int_value) for char in machine.stdout ])

    return render_template(
        "emulator.html",
        instruction=instruction_view,
        registers=registers_view,
        disassembled=disassembled_view,
        memory=memory_view,
        stdout=stdout_view,
        available_actions=available_actions
    )

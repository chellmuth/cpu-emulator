from dataclasses import dataclass
from typing import List

from flask import render_template, redirect

import assembler
from app import app
from core import Byte, Word, Register
from emulator import Machine

@dataclass
class DisassembledInstructionView:
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
        "ADD ra, 0x10000001",
        "STB ra, 0x50",
        "ADD rb, 0x01000000",
        "ORR ra, 0x10010000",
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

    address = 0
    instruction_views = []
    for instruction in machine.glob_instructions(0):
        instruction_views.append(
            DisassembledInstructionView(
                address,
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
    memory_view = MemoryView(2, [
        MemoryRowView(
            address * 8,
            [
                memory.read_word(address * 8 + 0).hex_str(),
                memory.read_word(address * 8 + 4).hex_str(),
            ]
        )
        for address in range(memory.size // (2 * 8))
    ])

    available_actions = set()
    if instruction:
        available_actions.add("step")

    return render_template(
        "emulator.html",
        instruction=instruction_view,
        registers=registers_view,
        disassembled=disassembled_view,
        memory=memory_view,
        available_actions=available_actions
    )

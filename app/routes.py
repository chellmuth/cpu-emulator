from dataclasses import dataclass
from typing import List

from flask import render_template, redirect

import assembler
from app import app
from core import Byte, Word, Register
from emulator import Machine

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
program = []

def reset_app():
    global program
    global machine

    program = [
        "ADD ra, 0x10000000",
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
    instruction_text = program.pop(0).strip()
    instruction = assembler.parse_to_instruction(instruction_text)

    machine.run(instruction)

    return render_emulator()

@app.route('/reset', methods=["POST"])
def reset():
    reset_app()

    return redirect("/")

def render_emulator():
    if not program:
        instruction_view = "--"
    else:
        instruction_view = program[0].strip()
        instruction_view = machine.next_instruction().human()

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
    if program:
        available_actions.add("step")

    return render_template(
        "emulator.html",
        instruction=instruction_view,
        registers=registers_view,
        memory=memory_view,
        available_actions=available_actions
    )

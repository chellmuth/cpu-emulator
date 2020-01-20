from dataclasses import dataclass

from flask import render_template

import assembler
from app import app
from emulator import Machine

@dataclass
class RegisterView:
    name: str
    value: str

program = [
    "ADD ra, 0x10000000",
    "ADD ra, 0x20000000",
    "ADD ra, 0x30000000",
]
print(program)

machine = Machine()

@app.route('/')
def hello_world():
    instruction_text = program.pop(0).strip()
    instruction = assembler.parse_to_instruction(instruction_text)

    machine.run(instruction)

    registers_view = [
        RegisterView("ra", machine.registers[0].hex_str() ),
        RegisterView("rb", machine.registers[1].hex_str() ),
    ]

    instruction_view = instruction.human()

    return render_template(
        "emulator.html",
        instruction=instruction_view,
        registers=registers_view,
    )

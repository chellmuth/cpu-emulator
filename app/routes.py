from dataclasses import dataclass

from flask import render_template

from app import app
from emulator import Machine

@dataclass
class RegisterView:
    name: str
    value: str

program_file = "./program.txt"
program = open(program_file).readlines()
print(program)

machine = Machine()

@app.route('/')
def hello_world():
    instruction = program.pop(0).strip()

    registers = [
        RegisterView("ra", machine.registers[0].hex_str()),
        RegisterView("rb", machine.registers[1].hex_str()),
    ]

    return render_template(
        "emulator.html",
        instruction=instruction,
        registers=registers,
    )

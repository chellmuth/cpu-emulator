from dataclasses import dataclass

from flask import render_template

from app import app

@dataclass
class RegisterView:
    name: str
    value: str

program_file = "./program.txt"
program = open(program_file).readlines()
print(program)

@app.route('/')
def hello_world():
    instruction = program.pop(0).strip()

    registers = [
        RegisterView("ra", "0x01"),
        RegisterView("rb", "0x0112"),
    ]

    return render_template(
        "emulator.html",
        instruction=instruction,
        registers=registers,
    )

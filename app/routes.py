from dataclasses import dataclass

from flask import render_template, redirect

import assembler
from app import app
from emulator import Machine

@dataclass
class RegisterView:
    name: str
    value: str

machine = None
program = []

def reset_app():
    global program
    global machine

    program = [
        "ADD ra, 0x10000000",
        "ADD rb, 0x01000000",
        "ORR ra, 0x10010000",
        "ADD ra, rb",
        "ADD ra, 0x30000000",
    ]

    machine = Machine()

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

    registers_view = [
        RegisterView("ra", machine.registers[0].hex_str() ),
        RegisterView("rb", machine.registers[1].hex_str() ),
    ]

    available_actions = set()
    if program:
        available_actions.add("step")

    return render_template(
        "emulator.html",
        instruction=instruction_view,
        registers=registers_view,
        available_actions=available_actions
    )

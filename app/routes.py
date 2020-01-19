from dataclasses import dataclass

from flask import render_template

from app import app

@dataclass
class RegisterView:
    name: str
    value: str

@app.route('/')
def hello_world():
    registers = [
        RegisterView("ra", "0x01"),
        RegisterView("rb", "0x0112"),
    ]
    return render_template("emulator.html", registers=registers)

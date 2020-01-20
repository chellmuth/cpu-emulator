import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class PushRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("PSH", value_register)

    def run(self, machine):
        dest = machine.registers[Register.sp]
        return MachineUpdate(
            memory={
                dest: machine.registers[self.value_register]
            },
            registers={
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

class PushConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("PSH", value_word)

    def run(self, machine):
        dest = machine.registers[Register.sp]
        return MachineUpdate(
            memory={
                dest: self.value_word
            },
            registers={
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class CallRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("CAL", value_register)

    def run(self, machine):
        return_pointer = machine.registers[Register.pc].incremented(self.size)
        increment_amount = machine.registers[self.value_register]

        return MachineUpdate(
            memory={
                machine.registers[Register.sp]: return_pointer
            },
            registers={
                Register.pc: machine.registers[Register.pc].incremented(increment_amount),
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

class CallConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("CAL", value_word)

    def run(self, machine):
        return_pointer = machine.registers[Register.pc].incremented(self.size)
        increment_amount = self.value_word.int_value()

        return MachineUpdate(
            memory={
                machine.registers[Register.sp]: return_pointer
            },
            registers={
                Register.pc: machine.registers[Register.pc].incremented(increment_amount),
                Register.sp: machine.registers[Register.sp].incremented(-4)
            }
        )

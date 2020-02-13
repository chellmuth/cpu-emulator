import instruction_base
from core import Byte, MachineUpdate, Register, Word

class InputRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("INP", value_register)

    def run(self, machine):
        user_input = input()
        user_int = ord(user_input[0])
        user_byte = Byte(user_int)

        return MachineUpdate(
            memory={
                machine.registers[self.value_register]: user_byte
            },
        )

class InputConstantInstruction(instruction_base.Type2ConstantInstruction):
    def __init__(self, value_word):
        super().__init__("INP", value_word)

    def run(self, machine):
        user_input = input()
        user_char = chr(user_input[0])
        user_byte = Byte(user_char)

        raise "Unimplemented!"

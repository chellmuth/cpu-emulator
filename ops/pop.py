import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class PopRegisterInstruction(instruction_base.Type2RegisterInstruction):
    def __init__(self, value_register):
        super().__init__("POP", value_register)

    def run(self, machine):
        pop_address = machine.registers[Register.sp].incremented(4)
        payload = machine.memory.read_word(pop_address.int_value())

        return MachineUpdate(
            registers={
                self.value_register: payload,
                Register.sp: pop_address
            }
        )

import instruction_base
from core import Register, Word
from emulator import MachineUpdate

class RetInstruction(instruction_base.Instruction):
    size = 1

    def human(self):
        return "RET"

    def run(self, machine):
        pop_address = machine.registers[Register.sp].incremented(4)
        updated_pc = machine.memory.read_word(machine.registers[Register.sp].int_value())

        return MachineUpdate(
            registers={
                Register.pc: updated_pc,
                Register.sp: pop_address
            }
        )

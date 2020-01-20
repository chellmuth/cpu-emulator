import instruction_base
from core import MachineUpdate, Register, Word

class RetInstruction(instruction_base.Instruction):
    size = 1

    def human(self):
        return "RET"

    def run(self, machine):
        updated_sp_address = machine.registers[Register.sp].incremented(4)
        popped_pc = machine.memory.read_word(updated_sp_address.int_value())

        return MachineUpdate(
            registers={
                Register.pc: popped_pc,
                Register.sp: updated_sp_address
            }
        )

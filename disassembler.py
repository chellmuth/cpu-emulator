import sys

import instruction
import ops
import ops.nop
import ops.ret
from byte_stream import BitStream
from core import Register, Word

def disassemble(filename):
    stream = BitStream.from_filename(filename)

    while not stream.is_empty():
        next_instruction = disassemble_instruction(stream)
        if not next_instruction: break

        print(next_instruction.human())

op_names = {
    0b010: ops.type_1_op_names,
    0b011: ops.type_1_op_names,
    0b100: ops.type_2_op_names,
    0b101: ops.type_2_op_names,
}

def disassemble_instruction(stream, strict=False):
    if stream.is_empty(): return

    type_code, = stream.read_int(3)
    # print("type code", bin(type_code))

    if type_code in op_names:
        if stream.is_empty():
            # Our file was padded with 7 bits to complete the byte
            # Made it look like we had an instruction when we don't
            return

        op_code, = stream.read_int(4)
        # print("op code:", op_code)
        op_name = op_names[type_code][op_code]
    elif type_code == 0b110:
        # todo: will crash if these are the last bits of a stream
        # and we got here due to padding
        op_name = "RET"
    elif type_code == 0b111:
        op_name = "NOP"
    else:
        if strict:
            raise ValueError
        else:
            return

    if type_code == 0b010:
        source, = stream.read_int(4)
        source_out = Register(source).name

        dest, = stream.read_int(4)
        dest_out = Register(dest).name

        skip, = stream.read_int(6)
        assert(skip == 0)

        return instruction.type1_register_factory(
            op_name, Register(source), Register(dest)
        )
    elif type_code == 0b011:
        dest, = stream.read_int(4)
        dest_out = Register(dest).name

        skip, = stream.read_int(3)
        assert(skip == 0)

        source_word = Word(*stream.read_bytes(4))
        source_out = source_word.hex_str()

        return instruction.type1_constant_factory(
            op_name, Register(dest), source_word
        )
    elif type_code == 0b100:
        value, = stream.read_int(4)
        value_out = Register(value).name

        skip, = stream.read_int(3)
        assert(skip == 0)

        return instruction.type2_register_factory(
            op_name, Register(value)
        )

    elif type_code == 0b101:
        value_word = Word(*stream.read_bytes(4))
        value_out = value_word.hex_str()

        return instruction.type2_constant_factory(
            op_name, value_word
        )
    elif type_code == 0b110:
        skip, = stream.read_int(4)
        assert(skip == 0)

        return ops.ret.RetInstruction()
    elif type_code == 0b111:
        skip, = stream.read_int(4)
        assert(skip == 0)

        return ops.nop.NopInstruction()

    else:
        if strict:
            raise ValueError
        else:
            return

if __name__ == "__main__":
    disassemble(sys.argv[1])

import instruction_base
import ops.add
import ops.bitwise_and
import ops.bitwise_not
import ops.bitwise_or
import ops.bitwise_xor
import ops.call
import ops.compare
import ops.input_op
import ops.jump
import ops.load
import ops.out
import ops.pop
import ops.push
import ops.store
import ops.subtract
import ops.test

def type1_register_factory(op_name, source_register, dest_register):
    cls_lookup = {
        "ADD": ops.add.AddRegisterInstruction,
        "SUB": ops.subtract.SubtractRegisterInstruction,
        "TST": ops.test.TestRegisterInstruction,
        "CMP": ops.compare.CompareRegisterInstruction,
        "AND": ops.bitwise_and.BitwiseAndRegisterInstruction,
        "ORR": ops.bitwise_or.BitwiseOrRegisterInstruction,
        "XOR": ops.bitwise_xor.BitwiseXorRegisterInstruction,
        "STR": ops.store.StoreWordRegisterInstruction,
        "STB": ops.store.StoreByteRegisterInstruction,
        "LOD": ops.load.LoadRegisterInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](source_register, dest_register)
    else:
        return instruction_base.Type1RegisterInstruction(
            op_name,
            source_register,
            dest_register
        )

def type1_constant_factory(op_name, dest_register, source_word):
    cls_lookup = {
        "ADD": ops.add.AddConstantInstruction,
        "SUB": ops.subtract.SubtractConstantInstruction,
        "TST": ops.test.TestConstantInstruction,
        "CMP": ops.compare.CompareConstantInstruction,
        "AND": ops.bitwise_and.BitwiseAndConstantInstruction,
        "ORR": ops.bitwise_or.BitwiseOrConstantInstruction,
        "XOR": ops.bitwise_xor.BitwiseXorConstantInstruction,
        "STR": ops.store.StoreWordConstantInstruction,
        "STB": ops.store.StoreByteConstantInstruction,
        "LOD": ops.load.LoadConstantInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](dest_register, source_word)
    else:
        return instruction_base.Type1ConstantInstruction(
            op_name,
            dest_register,
            source_word
        )

def type2_register_factory(op_name, value_register):
    cls_lookup = {
        "JMP": ops.jump.JumpRelativeRegisterInstruction,
        "JLT": ops.jump.JumpRelativeLessThanRegisterInstruction,
        "JEQ": ops.jump.JumpRelativeEqualRegisterInstruction,
        "CAL": ops.call.CallRegisterInstruction,
        "PSH": ops.push.PushRegisterInstruction,
        "POP": ops.pop.PopRegisterInstruction,
        "OUT": ops.out.PrintRegisterInstruction,
        "INP": ops.input_op.InputRegisterInstruction,
        "AMP": ops.jump.JumpAbsoluteRegisterInstruction,
        "ALT": ops.jump.JumpAbsoluteLessThanRegisterInstruction,
        "ALT": ops.jump.JumpAbsoluteEqualRegisterInstruction,
        "NOT": ops.bitwise_not.BitwiseNotRegisterInstruction,
        "AAL": ops.call.CallAbsoluteRegisterInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](value_register)
    else:
        return instruction_base.Type2RegisterInstruction(op_name, value_register)

def type2_constant_factory(op_name, value_word):
    cls_lookup = {
        "JMP": ops.jump.JumpRelativeConstantInstruction,
        "JLT": ops.jump.JumpRelativeLessThanConstantInstruction,
        "JEQ": ops.jump.JumpRelativeEqualConstantInstruction,
        "CAL": ops.call.CallConstantInstruction,
        "PSH": ops.push.PushConstantInstruction,
        "OUT": ops.out.PrintConstantInstruction,
        "INP": ops.input_op.InputConstantInstruction,
        "AMP": ops.jump.JumpAbsoluteConstantInstruction,
        "ALT": ops.jump.JumpAbsoluteLessThanConstantInstruction,
        "AEQ": ops.jump.JumpAbsoluteEqualConstantInstruction,
        "AAL": ops.call.CallAbsoluteConstantInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](value_word)
    else:
        return instruction_base.Type2ConstantInstruction(op_name, value_word)

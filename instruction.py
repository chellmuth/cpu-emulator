import instruction_base
import ops.add
import ops.bitwise_and
import ops.bitwise_not
import ops.bitwise_or
import ops.bitwise_xor
import ops.call
import ops.jump
import ops.load
import ops.out
import ops.pop
import ops.push
import ops.store

def type1_register_factory(op_name, source_register, dest_register):
    cls_lookup = {
        "ADD": ops.add.AddRegisterInstruction,
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
        "CAL": ops.call.CallRegisterInstruction,
        "PSH": ops.push.PushRegisterInstruction,
        "POP": ops.pop.PopRegisterInstruction,
        "OUT": ops.out.PrintRegisterInstruction,
        "AMP": ops.jump.JumpAbsoluteRegisterInstruction,
        "NOT": ops.bitwise_not.BitwiseNotRegisterInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](value_register)
    else:
        return instruction_base.Type2RegisterInstruction(op_name, value_register)

def type2_constant_factory(op_name, value_word):
    cls_lookup = {
        "JMP": ops.jump.JumpRelativeConstantInstruction,
        "CAL": ops.call.CallConstantInstruction,
        "PSH": ops.push.PushConstantInstruction,
        "OUT": ops.out.PrintConstantInstruction,
        "AMP": ops.jump.JumpAbsoluteConstantInstruction,
    }

    if op_name in cls_lookup:
        return cls_lookup[op_name](value_word)
    else:
        return instruction_base.Type2ConstantInstruction(op_name, value_word)

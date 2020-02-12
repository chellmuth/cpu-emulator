type_1_op_names = {
    0: "ADD",
    1: "SUB",
    2: "MUL",
    3: "DIV",
    4: "CMP",
    5: "TST",
    6: "AND",
    7: "ORR",
    8: "XOR",
    9: "STR",
    10: "STB",
    11: "LOD",
}

type_2_op_names = {
    0: "JMP",
    1: "JLT",
    2: "JEQ",
    3: "CAL",
    4: "PSH",
    5: "POP",
    6: "NOT",
    7: "OUT",
    8: "INP",
    9: "AMP",
    10: "ALT",
    11: "AEQ",
    12: "AAL",
}

op_codes = {
    value: key
    for lookup in [ type_1_op_names, type_2_op_names ]
    for key, value in lookup.items()
}

from binaryninja import (Architecture, RegisterInfo, InstructionInfo,
    InstructionTextToken, InstructionTextTokenType, InstructionTextTokenContext,
    BranchType,
    LowLevelILOperation, LLIL_TEMP,
    LowLevelILLabel,
    FlagRole,
    LowLevelILFlagCondition,
    log_error,
    CallingConvention,
    interaction,
    PluginCommand, BackgroundTaskThread,
    HighlightStandardColor
)

import struct

class Tigress1(Architecture):
    name = "tigress1"
    address_size = 8
    default_int_size = 8
    max_instr_length = 9

    regs = {"vsp": RegisterInfo("vsp", 8)}
    stack_pointer = "vsp"

    def get_instruction_info(self, data, address):
        opcode = data[0]

        if opcode == 0x60:
            # loadq
            result = InstructionInfo()
            result.length = 9
            return result
        elif opcode == 0x4e:
            # nop
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0xc7:
            # mulq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x8e:
            # ldarg
            result = InstructionInfo()
            result.length = 5
            return result
        elif opcode == 0x61:
            # rmem
            result = InstructionInfo()
            result.length = 1
            return result
        else:
            return None
    
    def get_instruction_text(self, data, address):
        opcode = data[0]

        if opcode == 0x60:
            # loadq
            immediate = struct.unpack("<Q", data[1:9])[0]

            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "loadq"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(immediate), immediate))
            return tokens, 9
        elif opcode == 0x4e:
            # nop
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "nop"))
            return tokens, 1
        elif opcode == 0xc7:
            # mulq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "mulq"))
            return tokens, 1
        elif opcode == 0x8e:
            # ldspcl
            immediate = struct.unpack("<L", data[1:5])[0]

            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "ldarg"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(immediate), immediate))
            return tokens, 5
        elif opcode == 0x61:
            # rmem
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "rmem"))
            return tokens, 1
        else:
            return None
    
    def get_instruction_low_level_il(self, data, address, il):
        opcode = data[0]

        if opcode == 0x60:
            # loadq
            immediate = struct.unpack("<Q", data[1:9])[0]
            il.append(il.push(8, il.const(8, immediate)))
            return 9
        elif opcode == 0x4e:
            # nop
            il.append(il.nop())
            return 1
        elif opcode == 0xc7:
            # mulq
            product = il.mult(8, il.pop(8), il.pop(8))
            il.append(il.push(8, product))
            return 1
        elif opcode == 0x8e:
            # ldarg
            immediate = struct.unpack("<L", data[1:5])[0]
            il.append(il.push(8, il.const(8, immediate)))
            return 5
        elif opcode == 0x61:
            # rmem
            il.append(il.push(8, il.load(8, il.pop(8))))
            return 1
        else:
            return None

Tigress1.register()

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
        else:
            return None
    
    def get_instruction_low_level_il(self, data, address, il):
        opcode = data[0]

        if opcode == 0x60:
            # loadq
            immediate = struct.unpack("<Q", data[1:9])[0]

            il.append(il.push(8, il.const(8, immediate)))
            return 9
        else:
            return None

Tigress1.register()

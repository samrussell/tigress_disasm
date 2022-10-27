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

    regs = {
        "vsp": RegisterInfo("vsp", 8),
        "varg1": RegisterInfo("varg1", 8),
        "varg2": RegisterInfo("varg2", 8),
        "vreg": RegisterInfo("vreg", 8),
        "vlhs": RegisterInfo("vlhs", 8),
        "vrhs": RegisterInfo("vrhs", 8),
    }
    stack_pointer = "vsp"

    def get_instruction_info(self, data, address):
        opcode = data[0]

        if opcode == 0x60 or opcode == 0xe1:
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
        elif opcode == 0x61 or opcode == 0x6e:
            # rmem
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x0e or opcode == 0x5f or opcode == 0x3c or opcode == 0x27:
            # addq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x90:
            # lead
            result = InstructionInfo()
            result.length = 5
            return result
        elif opcode == 0xdf:
            # wmem
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x56:
            # orq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x4a:
            # andq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x42:
            # subq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x5d:
            # shlq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0x2b:
            # shrq
            result = InstructionInfo()
            result.length = 1
            return result
        elif opcode == 0xf4:
            # jmp
            immediate = struct.unpack("<L", data[1:5])[0]
            result = InstructionInfo()
            result.length = 5
            result.add_branch(BranchType.UnconditionalBranch, address+immediate+1)
            return result
        elif opcode == 0x4d:
            # ret
            result = InstructionInfo()
            result.length = 1
            result.add_branch(BranchType.FunctionReturn, 0)
            return result
        else:
            return None
    
    def get_instruction_text(self, data, address):
        opcode = data[0]

        if opcode == 0x60 or opcode == 0xe1:
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
            # ldarg
            immediate = struct.unpack("<L", data[1:5])[0]

            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "ldarg"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(immediate), immediate))
            return tokens, 5
        elif opcode == 0x61 or opcode == 0x6e:
            # rmem
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "rmem"))
            return tokens, 1
        elif opcode == 0x0e or opcode == 0x5f or opcode == 0x3c or opcode == 0x27:
            # addq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "addq"))
            return tokens, 1
        elif opcode == 0x90:
            # lead
            immediate = struct.unpack("<L", data[1:5])[0]

            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "lead"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(immediate), immediate))
            return tokens, 5
        elif opcode == 0xdf:
            # wmem
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "wmem"))
            return tokens, 1
        elif opcode == 0x56:
            # orq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "orq"))
            return tokens, 1
        elif opcode == 0x4a:
            # andq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "andq"))
            return tokens, 1
        elif opcode == 0x42:
            # subq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "subq"))
            return tokens, 1
        elif opcode == 0x5d:
            # shlq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "shlq"))
            return tokens, 1
        elif opcode == 0x2b:
            # shrq
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "shrq"))
            return tokens, 1
        elif opcode == 0xf4:
            # jmp
            immediate = struct.unpack("<L", data[1:5])[0]

            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "jmp"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(immediate), immediate))
            return tokens, 5
        elif opcode == 0x4d:
            # ret
            tokens = []
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "ret"))
            return tokens, 1
        else:
            return None
    
    def get_instruction_low_level_il(self, data, address, il):
        opcode = data[0]

        if opcode == 0x60 or opcode == 0xe1:
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
            # needs more work
            if immediate == 0:
                varg = il.add(8, il.reg(8, "varg1"), il.const(4, immediate))
            elif immediate == 1:
                varg = il.add(8, il.reg(8, "varg2"), il.const(4, immediate))
            il.append(il.push(8, varg))
            return 5
        elif opcode == 0x61 or opcode == 0x6e:
            # rmem
            il.append(il.push(8, il.load(8, il.pop(8))))
            return 1
        elif opcode == 0x0e or opcode == 0x5f or opcode == 0x3c or opcode == 0x27:
            # addq
            sum = il.add(8, il.pop(8), il.pop(8))
            il.append(il.push(8, sum))
            return 1
        elif opcode == 0x90:
            # lead
            immediate = struct.unpack("<L", data[1:5])[0]
            vreg = il.add(8, il.reg(8, "vreg"), il.const(4, immediate))
            il.append(il.push(8, vreg))
            return 5
        elif opcode == 0xdf:
            # wmem
            il.append(il.set_reg(8, "vlhs", il.pop(8)))
            il.append(il.set_reg(8, "vrhs", il.pop(8)))
            il.append(il.store(8, il.reg(8, "vlhs"), il.reg(8, "vrhs")))
            return 1
        elif opcode == 0x56:
            # orq
            product = il.or_expr(8, il.pop(8), il.pop(8))
            il.append(il.push(8, product))
            return 1
        elif opcode == 0x4a:
            # andq
            product = il.and_expr(8, il.pop(8), il.pop(8))
            il.append(il.push(8, product))
            return 1
        elif opcode == 0x42:
            # subq
            il.append(il.set_reg(8, "vlhs", il.pop(8)))
            il.append(il.set_reg(8, "vrhs", il.pop(8)))
            sum = il.sub(8, il.reg(8, "vlhs"), il.reg(8, "vrhs"))
            il.append(il.push(8, sum))
            return 1
        elif opcode == 0x5d:
            # shlq
            il.append(il.set_reg(8, "vlhs", il.pop(8)))
            il.append(il.set_reg(8, "vrhs", il.pop(8)))
            sum = il.shift_left(8, il.reg(8, "vlhs"), il.reg(8, "vrhs"))
            il.append(il.push(8, sum))
            return 1
        elif opcode == 0x2b:
            # shrq
            il.append(il.set_reg(8, "vrhs", il.pop(8)))
            il.append(il.set_reg(8, "vlhs", il.pop(8)))
            sum = il.logical_shift_right(8, il.reg(8, "vlhs"), il.reg(8, "vrhs"))
            il.append(il.push(8, sum))
            return 1
        elif opcode == 0xf4:
            # jmp
            immediate = struct.unpack("<L", data[1:5])[0]
            dest = immediate + address + 1
            il.append(il.jump(il.const(8, dest)))
            return 5
        elif opcode == 0x4d:
            # ret
            il.append(il.ret(0))
            return 1
        else:
            return None

Tigress1.register()

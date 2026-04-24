import _exhaust_ma

from enum import Enum
import os
from .instruction import Instruction


class AsmLine(Enum):
    PIN = -3
    ORG = -2
    DONE = -1
    NONE = 0
    OK = 1


class Warrior:
    def __init__(self, warrior_pt):
        self.warrior_pt = warrior_pt
        self.name = None

    @property
    def code_ptr(self):
        return self.warrior_pt.code

    def __len__(self):
        return self.warrior_pt.len

    def __repr__(self):
        if self.name is not None:
            return "Warrior(name={!r})".format(self.name)
        else:
            return "Warrior({})".format(self.warrior_pt)

    def __getitem__(self, i):
        if i < 0:
            i = self.warrior_pt.len + i
        if i >= self.warrior_pt.len:
            raise IndexError("index out of range")

        return Instruction.from_insn_t(self.warrior_pt.code[i])

    def __str__(self):
        return "\n".join(
            str(instruction) if instruction.start_flag else f"      {instruction}"
            for instruction in self
        )

    @classmethod
    def from_filename(cls, core_settings, filename):
        # TODO: get filename etc from comments in the redcode source

        warrior_pt = _exhaust_ma.ffi.new("warrior_t*")
        _exhaust_ma.lib.asm_fname(
            str(filename).encode("utf-8"), warrior_pt, core_settings.core_size
        )
        instance = cls(warrior_pt)
        instance.name = os.path.basename(filename)
        return instance

    @classmethod
    def from_file(cls, core_settings, fp):
        return cls.from_lines(core_settings, fp)

    @classmethod
    def from_lines(cls, core_settings, lines):
        warrior_pt = _exhaust_ma.ffi.new("warrior_t*")
        i = 0
        for line in lines:
            instruction_result = _exhaust_ma.ffi.new("insn_t*")
            result = AsmLine(
                _exhaust_ma.lib.asm_line(
                    line.encode("utf-8"), instruction_result, core_settings.core_size
                )
            )
            if result == AsmLine.OK:
                warrior_pt.code[i] = {
                    k: getattr(instruction_result, k) for k in ["in", "a", "b"]
                }
                if getattr(instruction_result, "in") & 0b0100000000000000:
                    warrior_pt.start = i
                i += 1
            elif result == AsmLine.NONE:
                pass
            elif result == AsmLine.DONE:
                break
            elif result == AsmLine.ORG:
                warrior_pt.start = instruction_result.a
            elif result == AsmLine.PIN:
                warrior_pt.pin = instruction_result.a
                warrior_pt.have_pin = True
            else:
                assert False, "Unexpected return value from asm_line: {!r}".format(
                    result
                )

        warrior_pt.len = i

        instance = cls(warrior_pt)
        return instance

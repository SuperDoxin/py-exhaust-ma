import _exhaust_ma

from enum import Enum
import os


class Opcode(Enum):
    DAT = 0
    SPL = 1
    MOV = 2
    DJN = 3
    ADD = 4
    JMZ = 5
    SUB = 6
    SEQ = 7
    SNE = 8
    SLT = 9
    JMN = 10
    JMP = 11
    NOP = 12
    MUL = 13
    MODM = 14
    DIV = 15
    LDP = 16
    STP = 17


class Modifier(Enum):
    F = 0
    A = 1
    B = 2
    AB = 3
    BA = 4
    X = 5
    I = 6  # noqa: E741


class Mode(Enum):
    DIRECT = 0
    IMMEDIATE = 1
    BINDIRECT = 2
    BPREDEC = 3
    BPOSTINC = 4
    AINDIRECT = 5
    APREDEC = 6
    APOSTINC = 7

    @property
    def sigil(self):
        if self == Mode.DIRECT:
            return "$"
        if self == Mode.IMMEDIATE:
            return "#"
        if self == Mode.BINDIRECT:
            return "@"
        if self == Mode.BPREDEC:
            return "<"
        if self == Mode.BPOSTINC:
            return ">"
        if self == Mode.AINDIRECT:
            return "*"
        if self == Mode.APREDEC:
            return "{"
        if self == Mode.APOSTINC:
            return "}"
        assert False


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

    def __str__(self):
        out = []

        for i in range(self.warrior_pt.len):
            opcode = self.warrior_pt.code[i]
            in_ = getattr(opcode, "in")
            a = opcode.a
            b = opcode.b

            a_mode = Mode((in_ & 0b0000000000000111) >> 0)
            b_mode = Mode((in_ & 0b0000000000111000) >> 3)
            modifier = Modifier((in_ & 0b0000000111000000) >> 6)
            opcode = Opcode((in_ & 0b0001111000000000) >> 9)
            flags_start = bool(in_ & 0b0100000000000000)

            out.append(
                "{:>6} {}.{} {}{}, {}{}".format(
                    "start:" if flags_start else "",
                    opcode.name,
                    modifier.name,
                    a_mode.sigil,
                    a,
                    b_mode.sigil,
                    b,
                )
            )

        return "\n".join(out)

    @classmethod
    def from_filename(cls, core_settings, filename):
        # TODO: get filename etc from comments in the redcode source

        warrior_pt = _exhaust_ma.ffi.new("warrior_t*")
        _exhaust_ma.lib.asm_fname(
            filename.encode("utf-8"), warrior_pt, core_settings.core_size
        )
        instance = cls(warrior_pt)
        instance.name = os.path.basename(filename)
        return instance

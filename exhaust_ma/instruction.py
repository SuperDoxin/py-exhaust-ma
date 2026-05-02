from enum import Enum
from dataclasses import dataclass


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
    MOD = 14
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


@dataclass
class Field:
    mode: Mode
    value: int

    def __str__(self):
        return f"{self.mode.sigil}{self.value}"

    def __repr__(self):
        return f"Field({self})"


@dataclass
class Instruction:
    opcode: Opcode
    modifier: Modifier
    a: Field
    b: Field
    start_flag: bool = False

    def __str__(self):
        return (
            f"{'START: ' if self.start_flag else ''}"
            f"{self.opcode.name}.{self.modifier.name} "
            f"{self.a}, {self.b}"
        )

    def __repr__(self):
        return f"Instruction({self})"

    @classmethod
    def from_insn_t(cls, instruction):
        in_ = getattr(instruction, "in")
        return Instruction(
            opcode=Opcode((in_ & 0b0001111000000000) >> 9),
            modifier=Modifier((in_ & 0b0000000111000000) >> 6),
            a=Field(Mode((in_ & 0b0000000000000111) >> 0), instruction.a),
            b=Field(Mode((in_ & 0b0000000000111000) >> 3), instruction.b),
            start_flag=bool(in_ & 0b0100000000000000),
        )

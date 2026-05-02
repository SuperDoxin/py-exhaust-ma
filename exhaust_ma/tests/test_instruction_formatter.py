from .. import Warrior, Core, CoreSettings


def test_instruction_formatter():
    cs = CoreSettings(warrior_count=1, core_size=19)
    w1 = Warrior.from_lines(
        cs,
        [
            "DAT.A $0, #1",
            "SPL.B *2, @3",
            "MOV.AB {4, }5",
            "DJN.BA <6, >7",
            "ADD.X $8, $9",
            "JMZ.F $10, $11",
            "SUB.I $11, $12",
            "SEQ.F $13, $14",
            "SNE.F $15, $16",
            "SLT.F $17, $18",
            "JMN.F $19, $20",
            "JMP.F $21, $22",
            "NOP.F $23, $24",
            "MUL.F $25, $26",
            "MOD.F $27, $28",
            "DIV.F $29, $30",
            "LDP.F $31, $32",
            "STP.F $33, $34",
        ],
    )

    with Core(cs) as c:
        c.load_warriors([w1])

        assert [str(instruction) for instruction in c] == [
            "DAT.A $0, #1",
            "SPL.B *2, @3",
            "MOV.AB {4, }5",
            "DJN.BA <6, >7",
            "ADD.X $8, $9",
            "JMZ.F $10, $11",
            "SUB.I $11, $12",
            "SEQ.F $13, $14",
            "SNE.F $15, $16",
            "SLT.F $17, $18",
            "JMN.F $0, $1",
            "JMP.F $2, $3",
            "NOP.F $4, $5",
            "MUL.F $6, $7",
            "MOD.F $8, $9",
            "DIV.F $10, $11",
            "DAT.F $12, $13",
            "SPL.F $14, $15",
            "DAT.F $0, $0",
        ]

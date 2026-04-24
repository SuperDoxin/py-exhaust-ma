from .. import Warrior, CoreSettings, Mode, Modifier, Opcode


def test_warrior_getitem():
    cs = CoreSettings()
    w = Warrior.from_lines(cs, ["ORG START", "START mov.f $0,$1", "dat.X #2,   <3"])

    assert w[0].a.mode == Mode.DIRECT
    assert w[1].modifier == Modifier.X
    assert w[0].opcode == Opcode.MOV
    assert str(w[0]) == "START: MOV.F $0, $1"
    assert w[-2].opcode == Opcode.MOV
    assert w[0].start_flag
    assert str(w) == "START: MOV.F $0, $1\n      DAT.X #2, <3"

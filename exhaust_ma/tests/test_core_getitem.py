from .. import Warrior, CoreSettings, Core, Opcode  # , Mode, Modifier, Opcode


def test_warrior_getitem():

    class MyCoreSettings(CoreSettings):
        core_size = 10
        warrior_count = 1
        max_cycles = 100

    cs = MyCoreSettings()
    w = Warrior.from_lines(cs, ["ORG START", "START mov.I $0,$1", "dat.X #2,   <3"])
    core = Core(cs)

    assert core[0].opcode == Opcode.DAT

    core.load_warriors([w])

    assert core[0].opcode == Opcode.MOV
    assert core[2].opcode == Opcode.DAT

    core.run()

    assert core[2].opcode == Opcode.MOV

    assert len(core) == MyCoreSettings.core_size

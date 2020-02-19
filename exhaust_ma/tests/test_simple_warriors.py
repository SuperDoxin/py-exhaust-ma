from .. import Warrior, Core, CoreSettings
from pkg_resources import resource_filename


def test_stalker_vs_imp():
    stalker = resource_filename("exhaust_ma", "exhaust-ma/stalker.rc")
    imp = resource_filename("exhaust_ma", "exhaust-ma/imp.rc")

    cs = CoreSettings()
    w1 = Warrior.from_filename(cs, stalker)
    w2 = Warrior.from_filename(cs, imp)

    c = Core(cs)
    c.load_warriors([w1, w2])

    result = c.run()

    assert w1 in result.alive
    assert w1 not in result.dead

    assert w2 not in result.alive
    assert w2 in result.dead


def test_stalker_vs_imp_vs_imp():
    stalker = resource_filename("exhaust_ma", "exhaust-ma/stalker.rc")
    imp = resource_filename("exhaust_ma", "exhaust-ma/imp.rc")

    class ThreeWayCoreSettings(CoreSettings):
        warrior_count = 3

    cs = ThreeWayCoreSettings()
    w1 = Warrior.from_filename(cs, stalker)
    w2 = Warrior.from_filename(cs, imp)
    w3 = Warrior.from_filename(cs, imp)

    c = Core(cs)
    c.load_warriors([w1, w2, w3])

    result = c.run()

    assert w1 in result.alive
    assert w1 not in result.dead

    assert w2 in result.alive
    assert w2 not in result.dead

    assert w3 in result.alive
    assert w3 not in result.dead

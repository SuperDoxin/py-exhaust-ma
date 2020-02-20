from .. import Warrior, Core, CoreSettings
from pkg_resources import resource_filename
import pytest


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


@pytest.mark.parametrize(
    "warrior_filename",
    [
        resource_filename("exhaust_ma", "exhaust-ma/stalker.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/jaguar.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/spl.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/imp.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/ptest4.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/ptest6.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/pin1a.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/ptest5.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/validate.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/pin1b.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/ptest3.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/pin2b.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/pin2a.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/ptest1.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/t/ptest2.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/stalker.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/fixed.rc"),
        resource_filename("exhaust_ma", "exhaust-ma/npaper2.rc"),
    ],
)
def test_from_file(warrior_filename):
    cs = CoreSettings()
    with open(warrior_filename) as fp:
        w1 = Warrior.from_file(cs, fp)

    w2 = Warrior.from_filename(cs, warrior_filename)

    assert w1.warrior_pt.start == w2.warrior_pt.start
    assert w1.warrior_pt.have_pin == w2.warrior_pt.have_pin
    assert w1.warrior_pt.pin == w2.warrior_pt.pin
    assert len(w1) == len(w2)

    for op1, op2 in zip(
        w1.warrior_pt.code[0 : len(w1)], w2.warrior_pt.code[0 : len(w2)]
    ):
        assert getattr(op1, "in") == getattr(op2, "in")
        assert op1.a == op2.a
        assert op1.b == op2.b


def test_stalker_vs_imp_from_file():
    stalker = resource_filename("exhaust_ma", "exhaust-ma/stalker.rc")
    imp = resource_filename("exhaust_ma", "exhaust-ma/imp.rc")

    cs = CoreSettings()
    with open(stalker) as fp:
        w1 = Warrior.from_file(cs, fp)
    w1.name = "stalker"

    with open(imp) as fp:
        w2 = Warrior.from_file(cs, fp)
    w2.name = "imp"

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

from .. import CoreSettings, Core
import pytest


def test_core_close():
    core = Core(CoreSettings())
    core.close()
    with pytest.raises(ValueError):
        core.run()


def test_core_close_with():
    with Core(CoreSettings()) as core:
        pass
    with pytest.raises(ValueError):
        core.run()


def test_core_close_multiple():
    core = Core(CoreSettings())
    core.close()
    core.close()


def test_core_open_block():
    c1 = Core(CoreSettings())
    with pytest.raises(ValueError):
        c2 = Core(CoreSettings())

    c1.close()
    c2 = Core(CoreSettings())
    c2.close()

from .. import CoreSettings
from dataclasses import FrozenInstanceError
import pytest


def test_modifying_core_settings():
    cs = CoreSettings()
    with pytest.raises(FrozenInstanceError):
        cs.warrior_count = 1

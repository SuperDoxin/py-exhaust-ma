import _exhaust_ma
import random
from collections import namedtuple

BattleResult = namedtuple("BattleResult", ["dead", "alive"])


class CoreSettings:
    core_size = 8000
    processes = 8000
    warrior_count = 2
    max_cycles = 80000

    def __setattr__(self, k, v):
        raise NotImplementedError("CoreSettings are immutable")


class Core:
    _core_exists = False

    def __init__(self, core_settings):
        if Core._core_exists:
            raise RuntimeError("A core already exists")
        Core._core_exists = True

        self.core_settings = core_settings

        # TODO pspace support
        self.core = _exhaust_ma.lib.sim_alloc_bufs(
            self.core_settings.warrior_count,
            self.core_settings.core_size,
            self.core_settings.processes,
            self.core_settings.max_cycles,
        )

        if self.core == _exhaust_ma.ffi.NULL:
            raise RuntimeError("Failed to alocate memory for core.")

        self.loaded_warriors = ()
        self.load_positions = ()

    def load_warriors(self, warriors, placement_jitter=0):
        if len(warriors) != self.core_settings.warrior_count:
            raise ValueError(
                "Amount of warriors passed mismatches with core settings. "
                "Got {} warriors but expected {}.".format(
                    len(warriors), self.core_settings.warrior_count
                )
            )

        _exhaust_ma.lib.sim_clear_core()
        warrior_interval = self.core_settings.core_size // len(warriors)
        load_positions = []
        for i, warrior in enumerate(warriors):
            pos = int((i - random.uniform(0, placement_jitter)) * warrior_interval)
            _exhaust_ma.lib.sim_load_warrior(pos, warrior.code_ptr, len(warrior))
            load_positions.append(pos)

        self.loaded_warriors = tuple(warriors)
        self.load_positions = tuple(load_positions)

    def run(self):
        if len(self.loaded_warriors) == 0:
            raise ValueError("No warriors loaded")

        warrior_position_tab = _exhaust_ma.ffi.new(
            "field_t war_position_tab[]", self.load_positions
        )
        warrior_death_tab = _exhaust_ma.ffi.new(
            "unsigned int war_death_tab[]", [0] * self.core_settings.warrior_count
        )

        alive_count = _exhaust_ma.lib.sim_mw(
            self.core_settings.warrior_count, warrior_position_tab, warrior_death_tab
        )
        dead_count = self.core_settings.warrior_count - alive_count

        dead_list = []
        alive_set = set(self.loaded_warriors)

        for dead_index in warrior_death_tab[0:dead_count]:
            dead_list.append(self.loaded_warriors[dead_index])
            alive_set.remove(self.loaded_warriors[dead_index])

        return BattleResult(dead=dead_list, alive=alive_set)

    def __del__(self):
        _exhaust_ma.lib.sim_free_bufs()
        Core._core_exists = False

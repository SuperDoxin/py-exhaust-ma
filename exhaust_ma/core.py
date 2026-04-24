import _exhaust_ma
import random
from .instruction import Instruction
from .warrior import Warrior
from dataclasses import dataclass


@dataclass
class BattleResult:
    dead: list[Warrior]
    alive: set[Warrior]


@dataclass(frozen=True)
class CoreSettings:
    core_size: int = 8000
    processes: int = 8000
    warrior_count: int = 2
    max_cycles: int = 80000
    pspace_size: int = 500


class Core:
    _core_exists = False
    _open = False

    def __init__(self, core_settings):
        if Core._core_exists:
            raise ValueError("a core already exists")
        Core._core_exists = True
        self._open = True

        try:
            self.core_settings = core_settings

            # TODO pspace support
            self.core = _exhaust_ma.lib.sim_alloc_bufs2(
                self.core_settings.warrior_count,
                self.core_settings.core_size,
                self.core_settings.processes,
                self.core_settings.max_cycles,
                self.core_settings.pspace_size,
            )

            if self.core == _exhaust_ma.ffi.NULL:
                raise RuntimeError("failed to alocate memory for core.")

            self.loaded_warriors = ()
            self.load_positions = ()
        except Exception:
            Core._core_exists = False
            self._open = False
            raise

    def __len__(self):
        return self.core_settings.core_size

    def __getitem__(self, i):
        if not self._open:
            raise ValueError("operation on closed core")

        if i < 0:
            i = self.core_settings.core_size + i
        if i >= self.core_settings.core_size:
            raise IndexError("index out of range")

        return Instruction.from_insn_t(self.core[i])

    def load_warriors(self, warriors, placement_jitter=0):
        if not self._open:
            raise ValueError("operation on closed core")

        if len(warriors) != self.core_settings.warrior_count:
            raise ValueError(
                "Amount of warriors passed mismatches with core settings. "
                "Got {} warriors but expected {}.".format(
                    len(warriors), self.core_settings.warrior_count
                )
            )

        _exhaust_ma.lib.sim_clear_core()
        _exhaust_ma.lib.sim_reset_pspaces()
        warrior_interval = self.core_settings.core_size // len(warriors)
        load_positions = []
        for i, warrior in enumerate(warriors):
            pos = int((i - random.uniform(0, placement_jitter)) * warrior_interval)
            _exhaust_ma.lib.sim_load_warrior(pos, warrior.code_ptr, len(warrior))
            load_positions.append(pos)

        self.loaded_warriors = tuple(warriors)
        self.load_positions = tuple(load_positions)

    def run(self):
        if not self._open:
            raise ValueError("operation on closed core")

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

    def close(self):
        if not self._open:
            return

        _exhaust_ma.lib.sim_free_bufs()
        Core._core_exists = False
        self._open = False

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

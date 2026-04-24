from . import Warrior, Core, CoreSettings
import importlib.resources

jaguar = importlib.resources.files("exhaust_ma") / "exhaust-ma" / "jaguar.rc"
imp = importlib.resources.files("exhaust_ma") / "exhaust-ma" / "imp.rc"

cs = CoreSettings()
w1 = Warrior.from_filename(cs, jaguar)
w2 = Warrior.from_filename(cs, imp)

c = Core(cs)
c.load_warriors([w1, w2])

print(c.run())

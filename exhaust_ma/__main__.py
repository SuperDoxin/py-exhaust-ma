from . import Warrior, Core, CoreSettings
from pkg_resources import resource_filename

jaguar = resource_filename("exhaust_ma", "exhaust-ma/jaguar.rc")
imp = resource_filename("exhaust_ma", "exhaust-ma/imp.rc")

cs = CoreSettings()
w1 = Warrior.from_filename(cs, jaguar)
w2 = Warrior.from_filename(cs, imp)

c = Core(cs)
c.load_warriors([w1, w2])

print(c.run())

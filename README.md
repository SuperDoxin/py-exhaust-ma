# Py-Exhaust-MA
![Tests](https://github.com/SuperDoxin/py-exhaust-ma/workflows/Tests/badge.svg?branch=master) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/SuperDoxin/Py-Exhaust-Ma) ![GitHub issues](https://img.shields.io/github/issues/SuperDoxin/Py-Exhaust-Ma) ![GitHub](https://img.shields.io/github/license/SuperDoxin/Py-Exhaust-Ma) ![Awesome?](https://img.shields.io/badge/awesome%3F-yes!-green)

[Exhaust-MA](https://github.com/martinus/exhaust-ma) is a highly optimized Redcode simulator. Py-Exhaust-MA is the python bindings for [Exhaust-MA](https://github.com/martinus/exhaust-ma).

## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install Py-Exhaust-MA.

```bash
pip install exhaust-ma
```

## Usage

```python
from exhaust_ma import Warrior, Core, CoreSettings

jaguar = "jaguar.rc"
imp = "imp.rc"

cs = CoreSettings()
w1 = Warrior.from_filename(cs, jaguar)
w2 = Warrior.from_filename(cs, imp)

c = Core(cs)
c.load_warriors([w1, w2])

print(c.run())
```

[Exhaust-MA](https://github.com/martinus/exhaust-ma) includes a set of warriors which you can access using setuptools pkg_resources:

```python
from pkg_resources import resource_filename

jaguar = resource_filename("exhaust_ma", "exhaust-ma/jaguar.rc")
```

A full list of included files can be found [In the exhaust-MA repository.](https://github.com/martinus/exhaust-ma)

## Contributing

To get going:

```bash
    # Clone the git repository
    git clone git@github.com:SuperDoxin/py-exhaust-ma.git

    cd py-exhaust-ma

    # Update the submodules. This is needed for building the exhaust-ma cffi
    # library
    git submodule init
    git submodule update

    # Create a virtual environment to prevent polluting your system python
    # installation
    python -m venv venv
    source venv/bin/activate/

    # Install requirements
    pip install -r requirements.txt

    # Activate pre-commit hooks
    pre-commit install

    # Build the exhaust-ma cffi library
    python exhaust_ma/build_cffi.py
```

At this point running

```bash
    python -m exhaust_ma
```

Should output

```
   BattleResult(dead=[Warrior(name='imp.rc')], alive={Warrior(name='jaguar.rc')})
```

If it doesn't something has gone wrong, If you need further assistance open an issue and include all the output of all the commands you have run and I'll see what I can do.

Pull requests are more than welcome. As long as you've installed the pre-commit hooks most code style issues should be checked automatically.

Updating/adding tests is appreciated but by no means a requirement for a PR to get accepted.

## License
[GNU GENERAL PUBLIC LICENSE Version 2](https://github.com/SuperDoxin/py-exhaust-ma/blob/master/LICENSE)

from setuptools import setup

setup(
    name="exhaust-ma",
    version="0.0.2",
    setup_requires=["cffi>=1.0.0", "wheel>=0.34.2"],
    cffi_modules=["exhaust_ma/build_cffi.py:ffi"],
    install_requires=["cffi>=1.0.0", "wheel>=0.34.2"],
    packages=["exhaust_ma"],
    author="Lieuwe Mosch",
    author_email="lieuwemo@gmail.com",
    description="Fast CoreWars redcode simulator, python bindings.",
    keywords="corewars redcode mars",
    include_package_data=True,
)

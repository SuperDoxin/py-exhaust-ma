from setuptools import setup

setup(
    cffi_modules=["exhaust_ma/build_cffi.py:ffi"],
    include_package_data=True,
)

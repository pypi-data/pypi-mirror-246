# -*- coding: utf-8 -*-
__author__ = 'chengzhi'

import setuptools

# from py-spy/setup.py
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package (we have platform specific lib)
            if self.plat_name != "any":
                self.root_is_pure = False
                self.distribution.package_data[""] = ["**"]

        def get_tag(self):
            # this set's us up to build generic wheels.
            python, abi, plat = _bdist_wheel.get_tag(self)
            # We don't contain any python source
            python, abi = 'py3', 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None

with open("README.md", mode="r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tqsdk2-fclib',
    version="2.2.8",
    description='TianQin SDK2 - fclib',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='TianQin',
    author_email='tianqincn@gmail.com',
    url='https://www.shinnytech.com/tqsdk',
    packages=["tqsdk2"],
    python_requires='>=3',
    cmdclass={'bdist_wheel': bdist_wheel},
)

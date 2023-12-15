from setuptools import setup, find_packages

setup(
	name='functional-swipl-interface',
	version='1.0.1',
	author='Lev Shuster',
	author_email='Shusterlev@gmail.com',
	description='A wrapper built on top of the official SWI-Prolog Python interface to iteract with prolog through python using a functional programming paradigm. This wrapper is specifically designed to facilitate programmers with no prior knowledge of logic programming to interact with Prolog',
	packages=find_packages(),
	license="MIT",
	readme = "README.md",
	install_requires=['swiplserver'],
	url = "https://github.com/levshuster/functional-swipl-interface",
)

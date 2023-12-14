from setuptools import setup, find_packages

setup(
	name='functional-swipl-interface',
	version='1.0.0',
	author='Lev Shuster',
	author_email='Shusterlev@gmail.com',
	description='A wrapper was built on top of the official SWI-Prolog Python interface to enable interaction with SWIPL using a functional programming paradigm. This wrapper is specifically designed to facilitate programmers with no prior knowledge of logic programming to interact with Prolog',
	packages=find_packages(),
)

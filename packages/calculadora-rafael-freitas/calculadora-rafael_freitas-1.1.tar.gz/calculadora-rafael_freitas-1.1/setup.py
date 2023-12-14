from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='calculadora-rafael_freitas',
    version=1.1,
    description='este pacote faz operações básicas',
    long_description=Path('README.md').read_text(encoding='utf-8'),
    author='Rafael Freitas',
    author_email='raf.mec.ba@gmail.com',
    keywords=['calculadora','operações','matemática'],
    packages=find_packages()
)
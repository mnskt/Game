import sys
from cx_Freeze import setup, Executable


setup(
    name='Synergy',
    version='1.0',
    description='2D game WIP',
    executables=[Executable('main.py', base='Win32GUI')]
)

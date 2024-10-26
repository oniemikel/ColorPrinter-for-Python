from .main import ColorPrinter, print
from yaml import safe_load

with open('././config.yml', 'r', encoding='utf-8') as file:
    __version__ = safe_load(file).get('version')
__all__ = ['ColorPrinter', 'print']
import os


def cursor_arriba(n=1):
    """sube el cursor n veces"""
    print(f'\033[{n}A', end="")


def raya():
    """escribe guiones a lo ancho de la pantalla"""
    print('-'*os.get_terminal_size().columns)
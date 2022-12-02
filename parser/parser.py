#!/usr/bin/env python3

from ctypes import sizeof
import sys, string
from CLI_class import CLI

def main():
    _CLI = CLI()
    _CLI.initialize()
    _CLI.get_arguments()
    _CLI.analyse_cli()
    _CLI.add_and_remove()

if __name__ == "__main__":
    main()
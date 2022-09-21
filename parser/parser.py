#!/usr/bin/env python3

from ctypes import sizeof
import sys, string
from parser_class import Parser


def main():
    _parser = Parser()
    _parser.initialize_flags()
    _parser.get_arguments()
    _parser.analyse_cli()



if __name__ == "__main__":
    print("innan main()")
    main()


#parser.py 
#print, add, -c ,-d, -path, pathen
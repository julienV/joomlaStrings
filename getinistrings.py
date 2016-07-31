#! /usr/bin/env python3

import re
import os
import argparse

class GetIniStrings:
    """Extract all language strings from ini files"""

    def __init__(self, basepath):
        self.__basepath = basepath
        self.__current = ''
        self.__found = {}

    def parse(self):
        for root, dirs, files in os.walk(self.__basepath):
            for filename in files:
                filepath = os.path.join(root, filename)
                self.__current = filepath

                if filename.endswith('.ini'):
                    self.__parseIni()

        return self.__found

    def findString(self, str):
        locations = []
        needle = str.upper()

        for key, val in self.__found.items():
            if needle in val:
                locations.append(key)

        return locations

    def printResults(self):
        for key, value in self.__found.items():
            self.__printFileHeader(key)
            for element in value:
                print(element)

    def __parseIni(self):
        f = open(self.__current, 'r')
        for line in f:
            m = re.match('([a-zA-Z_]+)=', line)
            if m:
                self.__addString(m.group(1))
        f.close()

    def __addString(self, string):
        if not self.__current in self.__found:
            self.__found[self.__current] = []

        if string in self.__found[self.__current]:
            print('String already defined in file', string)
            return

        self.__found[self.__current].append(string.upper())

    def __printFileHeader(self, filepath):
        print()
        print('#', os.path.relpath(filepath, self.__basepath))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parses all ini files, and find Joomla language strings.')
    parser.add_argument('-p', '--path', required=False, help='the base path to parse', default=os.getcwd())
    args = parser.parse_args()
    x = GetIniStrings(args.path)
    res = x.parse()
    x.printResults()

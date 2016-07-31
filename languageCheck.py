#! /usr/bin/env python3

import os
import argparse
from extractJtext import ExtractJtext
from getinistrings import GetIniStrings

class LanguageCheck:

    def __init__(self, basepath):
        self.basepath = basepath
        self.extract = ExtractJtext(self.basepath)
        self.iniStrings = GetIniStrings(self.basepath)

    def check(self):
        extracted = self.extract.parse()
        iniStrings = self.iniStrings.parse()

        for file, values in iniStrings.items():
            print(file)
            for iniString in values:
                if not self.extract.findString(iniString):
                    print('not used:', iniString)

        for file, values in extracted.items():
            notfound = []
            for str in values:
                if not self.iniStrings.findString(str):
                    notfound.append(str)

            if notfound:
                print(file)
                for str in notfound:
                    print('Not translated:', str)

    def loadIniStrings(self):
        for root, dirs, files in os.walk(self.basepath):
            for filename in files:
                filepath = os.path.join(root, filename)
                self.current = filepath

                if filename.endswith('.php'):
                    self.parsePhp()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check for consitency of language strings in designated path. Look for strings in all found ini files, and compare to all strings to be translated')
    parser.add_argument('-p', '--path', required=False, help='the base path to parse', default=os.getcwd())
    args = parser.parse_args()
    x = LanguageCheck(args.path)
    x.check()

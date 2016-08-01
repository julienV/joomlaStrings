#! /usr/bin/env python3

import os
import argparse
from extractJtext import ExtractJtext
from getinistrings import GetIniStrings

class LanguageCheck:

    def __init__(self, basepath, ignorepath=None, ignorestrings=None):
        self.basepath = basepath
        self.extract = ExtractJtext(self.basepath, ignorepath)
        self.iniStrings = GetIniStrings(self.basepath, ignorestrings)

    def check(self):
        extracted = self.extract.parse()
        iniStrings = self.iniStrings.parse()

        print('################  Unused strings ################')
        for file, values in iniStrings.items():
            notused = []

            for iniString in values:
                if not self.extract.findString(iniString):
                    notused.append(iniString)

            if notused:
                print('')
                print(file)
                for str in notused:
                    print(str)

        print('')
        print('################  Untranslated strings ################')
        for file, values in extracted.items():
            notfound = []
            for str in values:
                if not self.iniStrings.findString(str):
                    notfound.append(str)

            if notfound:
                print('')
                print(file)
                for str in notfound:
                    print(str)

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
    parser.add_argument('-ip', '--ignorepath', required=False, help='default ignore file, using unix pattern matching')
    parser.add_argument('-is', '--ignorestrings', required=False, help='default strings ignore file')
    args = parser.parse_args()
    x = LanguageCheck(args.path)
    x.check()

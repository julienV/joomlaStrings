#! /usr/bin/env python3

import re
import os
import argparse
import xml.etree.ElementTree as ET

class ExtractJtext:
    """Extract all language strings from php and xml files"""

    def __init__(self, basepath):
        self.__basepath = basepath
        self.__current = ''
        self.__found = {}

    def parse(self):
        for root, dirs, files in os.walk(self.__basepath):
            for filename in files:
                filepath = os.path.join(root, filename)
                self.__current = filepath

                if filename.endswith('.php'):
                    self.__parsePhp()

                if filename.endswith('.xml'):
                    self.__parseXml()

        return self.__found

    def printResults(self):
        for key, value in self.__found.items():
            self.__printFileHeader(key)
            for element in value:
                print(element)

    def findString(self, str):
        locations = []
        needle = str.upper()

        for key, val in self.__found.items():
            if needle in val:
                locations.append(key)

        return locations

    def __parsePhp(self):
        p = re.compile(r'JText::(?:_|sprintf|script)\(([\'"])(?P<lang>.+)\1')
        matches = p.findall(self.__getText(self.__current))

        if matches:
            for match in matches:
                self.__addString(match[1])

    def __parseXml(self):
        try:
            root = ET.parse(self.__current).getroot()
        except ET.ParseError:
            print('Error: Invalid xml', self.__current)
            return

        if root.tag == 'access':
            self.__parseXmlAccess(root)
        elif root.tag == 'config':
            self.__parseXmlConfig(root)
        elif root.tag == 'extension':
            self.__parseXmlExtension(root)
        elif root.tag == 'form':
            self.__parseXmlForm(root)

    def __parseXmlAccess(self, root):
        for el in root.findall(".//action"):
            self.__addString(el.get('title'))
            self.__addString(el.get('description'))

    def __parseXmlConfig(self, root):
        return self.__parseXmlForm(root)

    def __parseXmlExtension(self, root):
        if root.find('name') is not None:
            self.__addString(root.find('name').text)

        if root.find('description') is not None:
            self.__addString(root.find('description').text)

        for el in root.findall(".//menu"):
            self.__addString(el.text)

    def __parseXmlForm(self, root):
        for el in root.findall(".//action"):
            if el.get('label') is not None:
                self.__addString(el.get('label'))
            if el.get('description') is not None:
                self.__addString(el.get('description'))

        for el in root.findall(".//field"):
            if el.get('label') is not None:
                self.__addString(el.get('label'))
            if el.get('description') is not None:
                self.__addString(el.get('description'))

            for opt in el.findall("option"):
                self.__addString(opt.text)

    def __getText(self, filepath):
        textfile = open(filepath, 'r')
        filetext = textfile.read()
        textfile.close()
        return filetext

    def __printFileHeader(self, filepath):
        print()
        print('#', os.path.relpath(filepath, self.__basepath))

    def __addString(self, string):
        if not string:
            return

        if not self.__current in self.__found:
            self.__found[self.__current] = []

        self.__found[self.__current].append(string.upper())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parses a joomla file, and find language strings from php and xml files.')
    parser.add_argument('-p', '--path', required=False, help='the base path to parse', default=os.getcwd())
    args = parser.parse_args()
    x = ExtractJtext(args.path)
    res = x.parse()
    x.printResults()
    print(x.findString('JACTION_ADmIN'))

# author: i342722
# email : harshil.sokhadia@sap.com

from libs import DuplicateStrings
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="The android repo path without the '/' at the end.")
parser.add_argument("-j", "--jamstrings", help="force remove the jam strings", action="store_true")
parser.add_argument("-v", "--verbose", help="Displays all the duplicate strings in verbose fashion", action="store_true")
args = parser.parse_args()

if __name__ == '__main__':

        duplicate_module = DuplicateStrings.DuplicateStrings(args)

        duplicate_module.trim_all_modules()
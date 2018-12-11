# author: i342722
# email : harshil.sokhadia@sap.com

import sys

import Utils
from libs import TrimStrings
from libs import DuplicateStrings
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="The android repo path without the '/' at the end.")
parser.add_argument("-j", "--jamstrings", help="force remove the jam strings", action="store_true")
parser.add_argument("-v", "--verbose", help="Displays all the duplicate strings in verbose fashion", action="store_true")
parser.add_argument("-u", "--unused", help="Remove unused Strings", action="store_true")
parser.add_argument("-d", "--duplicate", help="Remove Duplicate Strings", action="store_true")
args = parser.parse_args()

if __name__ == '__main__':

    if args.jamstrings:
        print("WARNING: Jam String are force removed.")

    if args.unused:
        trim_module = TrimStrings.TrimStrings(args)
        print("INFO: Trimming App Module")
        trim_module.trim_app_module()
        print("INFO: App Module Trimmed.\n\n")

        print("INFO: Trimming Common Module")
        trim_module.trim_common_module()
        print("INFO: Common Module Trimmed.")

    if args.duplicate:
        duplicate_dict = defaultdict(list)
        duplicate_module = DuplicateStrings.DuplicateStrings(args)
        print("INFO: Looking for duplicate strings in App Module")
        duplicate_dict = duplicate_module.trim_duplicate_app_module()
        print("INFO: Lookup Done in App Module.\n\n")

        print("INFO: Looking for duplicate strings in Common Module")
        duplicate_dict.update(duplicate_module.trim_duplicate_common_module())
        print("INFO: Lookup Done in Common Module.\n\n")

        print("INFO: Removing duplicate strings")
        Utils.replace_duplicate_string_ref(duplicate_dict, args.path)
        print("INFO: Removing Done.")



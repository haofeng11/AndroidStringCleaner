# author: i342722
# email : harshil.sokhadia@sap.com

import Utils
import re
import lxml.etree as ET
import os


class TrimStrings:

    regex1 = "string\/([a-zA-Z_0-9]+)"
    regex2 = "R\.string\.([a-zA-Z_0-9]+)"
    regex3 = "R\.array\.([a-zA-Z_0-9]+)"
    regex4 = "R\.plurals\.([a-zA-Z_0-9]+)"
    args = ""

    repo_path = ""
    app_path = ""
    common_path = ""

    def __init__(self, args):
        self.args = args
        self.repo_path = args.path
        self.app_path = Utils.get_strings_path(self.repo_path)[0]
        self.common_path = Utils.get_strings_path(self.repo_path)[1]

    def trim_module(self, p):

        used_strings_set = set(re.findall(self.regex1,
                                          str(Utils.run_commmand('/usr/bin/grep -R \'@string/\' '+self.repo_path)[0])))
        source_usage_text = str(Utils.run_commmand('/usr/bin/grep -R \'R\.\' '+self.repo_path)[0])

        used_strings_set = used_strings_set.union(set(re.findall(self.regex2, source_usage_text)))
        used_strings_set = used_strings_set.union(set(re.findall(self.regex3, source_usage_text)))
        used_strings_set = used_strings_set.union(set(re.findall(self.regex4, source_usage_text)))

        tree = ET.parse(p+'/values/strings.xml')
        root = tree.getroot()

        elements = list()

        for element in root:
            elements.append(element)

        for element in elements:

            if 'name' in element.attrib and element.attrib['name'] not in used_strings_set:
                if not self.args.jamstrings:
                    if not element.attrib['name'].startswith('jam'):
                        if self.args.verbose:
                         print(element.attrib['name'])
                        root.remove(element)

                else:
                    if self.args.verbose:
                        print(element.attrib['name'])
                        root.remove(element)

        f = open(p+'/strings.xml', 'wb')
        f.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'.encode('utf-8'))
        tree.write(f, encoding='utf-8')

        f.flush()

    def trim_app_module(self):

        if self.args.verbose:
            print("INFO: Following strings will be removed from the app module")
        self.trim_module(self.app_path)
        return

    def trim_common_module(self):

        if self.args.verbose:
            print("INFO: Following strings will be removed from the common module")

        self.trim_module(self.common_path)
        return

    def trim_all_modules(self):
        self.trim_app_module()
        self.trim_common_module()

    # the functions below were to solve the GNG defects because of Strings
    def find_conflict_strings(self):
        used_strings_set = set(re.findall(self.regex1,
                                          str(Utils.run_commmand('/usr/bin/grep -R \'@string/\' ' + self.repo_path)[0])))
        source_usage_text = str(Utils.run_commmand('/usr/bin/grep -R \'R\.\' ' + self.repo_path)[0])

        used_strings_set = used_strings_set.union(set(re.findall(self.regex2, source_usage_text)))
        used_strings_set = used_strings_set.union(set(re.findall(self.regex3, source_usage_text)))
        used_strings_set = used_strings_set.union(set(re.findall(self.regex4, source_usage_text)))

        locale_path = self.repo_path + '/app/src/main/res/'

        tree = ET.parse(locale_path + 'values/strings.xml')
        root = tree.getroot()

        for element in root:
            if 'name' in element.attrib:
                if element.attrib['name'] in used_strings_set:
                    used_strings_set.remove(element.attrib['name'])

        locale_path = self.repo_path + '/common/src/main/res/';

        tree = ET.parse(locale_path + 'values/strings.xml')
        root = tree.getroot()

        for element in root:
            if 'name' in element.attrib:
                if element.attrib['name'] in used_strings_set:
                    used_strings_set.remove(element.attrib['name'])

        used_strings_set_itr = list(used_strings_set)

        for element in used_strings_set_itr:
            if element.startswith('fiori'):
                used_strings_set.remove(element)

        print(used_strings_set)
        exit(0)

    def check_for_crashes(self):
        locale_path = self.repo_path + '/app/src/main/res/'

        tree = ET.parse(locale_path + 'values/strings.xml')
        root = tree.getroot()

        default_elements = list()

        for element in root:
            if 'name' in element.attrib:
                default_elements.append(element.attrib['name'])

        for each_locale in Utils.LOCALES:

            if os.path.isfile(locale_path + each_locale + '/strings.xml'):
                tree = ET.parse(locale_path + each_locale + '/strings.xml')
                root = tree.getroot()
                elements = list()

                for element in root:
                    if 'name' in element.attrib:
                        elements.append(element.attrib['name'])

                print("In " + each_locale + " ,strings.xml")
                for element in default_elements:
                    if element in elements:
                        elements.remove(element)

                for element in elements:
                    print(element, end=', ')

    '''   def trim_all_locales(self,p,removed_strings_set):

           locales = ['values-ar', 'values-fr', 'values-ms', 'values-sv', 'values-bg', 'values-fr-rCA', 'values-nb', 'values-ca-rES',
                    'values-he', 'values-nl', 'values-cs', 'values-hi', 'values-no', 'values-th', 'values-cy', 'values-hr', 'values-pl',
                    'values-tr', 'values-da', 'values-hu', 'values-pt', 'values-uk', 'values-de', 'values-in', 'values-pt-rBR',
                    'values-el', 'values-it', 'values-ro', 'values-vi', 'values-en-rGB', 'values-iw', 'values-ru', 'values-es',
                    'values-ja', 'values-sk', 'values-es-rMX', 'values-ko', 'values-sl', 'values-zh', 'values-fi', 'values-sr',
                    'values-zh-rTW']

           #locales = find_all_locales_strings_path()



           used_strings_set = used_strings_set.union(set(re.findall(self.regex2, source_usage_text)))
           used_strings_set = used_strings_set.union(set(re.findall(self.regex3, source_usage_text)))
           used_strings_set = used_strings_set.union(set(re.findall(self.regex4, source_usage_text)))

           locale_path = self.repo_path+'/common/src/main/res/'

           tree = ET.parse(locale_path + 'values/strings.xml')
           root = tree.getroot()

           eng_elements = list()

           for element in root:
               if 'name' in element.attrib:
                   eng_elements.append(element.attrib['name'])

           for path in locales:

               if os.path.isfile(locale_path + path+'/strings.xml'):
                   tree = ET.parse(locale_path + path+'/strings.xml')
                   root = tree.getroot()
                   elements = list()

                   for element in root:
                       elements.append(element)
                   for element in elements:

                       if 'name' in element.attrib and (element.attrib['name'] not in eng_elements
                                                        and element.attrib['name'] not in used_strings_set):
                           if not self.args.jamstrings:
                               if not element.attrib['name'].startswith('jam'):
                                   if self.args.verbose:
                                       print(element.attrib['name'])
                                   root.remove(element)
                           else:
                               if self.args.verbose:
                                   print(element.attrib['name'])
                               root.remove(element)

                   f = open(locale_path + path + '/strings.xml', 'wb')
                   f.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'.encode('utf-8'))
                   tree.write(f, encoding='utf-8')


   '''



    def find_all_locales_strings_path(self):

        return [];



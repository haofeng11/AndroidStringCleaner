# author: i342722
# email : harshil.sokhadia@sap.com
import os
import subprocess
import lxml.etree as ET

global LOCALES
LOCALES = ['values-ar', 'values-fr', 'values-ms', 'values-sv', 'values-bg', 'values-fr-rCA', 'values-nb',
           'values-ca-rES',
           'values-he', 'values-nl', 'values-cs', 'values-hi', 'values-no', 'values-th', 'values-cy',
           'values-hr', 'values-pl',
           'values-tr', 'values-da', 'values-hu', 'values-pt', 'values-uk', 'values-de', 'values-in',
           'values-pt-rBR',
           'values-el', 'values-it', 'values-ro', 'values-vi', 'values-en-rGB', 'values-iw', 'values-ru',
           'values-es',
           'values-ja', 'values-sk', 'values-es-rMX', 'values-ko', 'values-sl', 'values-zh', 'values-fi',
           'values-sr',
           'values-zh-rTW']


def get_strings_path(p):
    if not os.path.isdir(p):
        raise Exception("Android Directory is not Valid")
    app_path = p + '/app/src/main/res'
    common_path = p + '/common/src/main/res'
    return [app_path, common_path]


def run_commmand(command, shell=True):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=shell)
    return proc.communicate()


def extract_elements_from_xml(file_path):
    if os.path.isfile(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        elements = list()
        for element in root:
            elements.append(element)
    return elements


def check_equal(lst):
    if not lst:
        return True

    first_ele = lst[0]

    for x in lst:
        if x != first_ele:
            return False

    return True


def remove_element_from_xml(path, remove_tags):

    if os.path.isfile(path):
        tree = ET.parse(path)
        root = tree.getroot()

        for element in root:
            if 'name' in element.attrib and element.attrib['name'] in remove_tags:
                root.remove(element)

        f = open(path, 'wb')
        f.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'.encode('utf-8'))
        tree.write(f, encoding='utf-8')

        f.flush()


def replace_java_command(duplicate_list, repo_path):
    origin_str = duplicate_list[0]
    for tag in duplicate_list[1:]:

        command = 'find  ' + str(repo_path) + '/app/src  ' + str(repo_path) + \
                  '/common/src -iname \"*.java\" -exec sed -i ' + \
                  "\"s/R.string." + str(tag) + '\\b/R.string.' + str(origin_str) + "/g\" {} +"
        run_commmand(command)


def replace_xml_command(duplicate_list, repo_path):
    origin_str = duplicate_list[0]
    for tag in duplicate_list[1:]:

        command = 'find  ' + str(repo_path) + '/app/src/main/res  ' + str(repo_path) + \
                  '/common/src/main/res -iname \"*.xml\" -exec sed -i ' + \
                  "\"s:@string/" + str(tag) + '\\b:@string/' + str(origin_str) + ":g\" {} +"
        run_commmand(command)


def replace_duplicate_string_ref(duplicate_dict, repo_path):
    for value_key in duplicate_dict:
        replace_java_command(duplicate_dict[value_key], repo_path)
        replace_xml_command(duplicate_dict[value_key], repo_path)


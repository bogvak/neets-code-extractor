from lxml import etree
import os, errno, sys

#Initial vars
init_string = '<?xml version="1.0" encoding="utf-8"?>\n'
args = []

#Initial defs
def save_project_file(full_file_path, full_tree):
    with open(full_file_path, 'w', encoding='utf-8') as file:
        print('Saving : ' + full_file_path)
        file.write(init_string+etree.tostring(full_tree, pretty_print=True, encoding='unicode'))


def open_project_file(file_name):
    full_tree = etree.parse(file_name)
    return full_tree


def save_code_to_file(code_dir, element):
    with open(code_dir+'/'+element.tag+'.pawn', 'w') as file:
        print("Extracting " + element.tag)
        file.write(element.text)


def decompile_neets(file_path, file_name):
    sys_code_dir = file_path + "\\_system_code"
    full_file_path = file_path + "\\" + file_name

    try:
        os.makedirs(sys_code_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    full_tree = open_project_file(full_file_path)
    node = get_system_code_el(full_tree)
    t = node.getchildren()
    for node in t:
        save_code_to_file(sys_code_dir, node)


def compile_neets(file_path, file_name):
    sys_code_dir = file_path + "\\_system_code"
    full_file_path = file_path + "\\" + file_name

    if not os.path.exists(sys_code_dir):
        print('no System Code to compile')
        return

    # clearing System Code
    full_tree = open_project_file(full_file_path)
    delete_all_elements_from_system_code(full_tree)
    node_system_code = get_system_code_el(full_tree)

    print("Using "+get_controller_version(full_tree)+" controller")

    files_to_compile = os.scandir(sys_code_dir)
    for next_file_to_compile in files_to_compile:
        if not next_file_to_compile.is_dir() :
            print("Adding "+next_file_to_compile.name)
            with open(sys_code_dir + '/' + next_file_to_compile.name) as next_file_desc:
                file_name, file_extension = os.path.splitext(os.path.basename(next_file_desc.name))
                new_node = etree.Element(file_name)
                new_node.text = ""
                if "-inc" in args:
                    for line in next_file_desc:
                        new_node.text = new_node.text + line
                        if "//|+|" == line[0:5]:
                            inc_file_name = sys_code_dir + "\\" + line[5:len(line)-1]
                            print("Trying to include: " + inc_file_name)
                            try:
                                with open(inc_file_name) as inc_file_name_desc:
                                    new_node.text = new_node.text + inc_file_name_desc.read() + "\n"
                                    new_node.text = new_node.text + "//|-|\n"
                            except IOError as error:
                                print("Can't include: " + inc_file_name)
                else:
                    new_node.text = next_file_desc.read()
                node_system_code.append(new_node)

    save_project_file(full_file_path, full_tree)


def delete_all_elements_from_system_code(full_tree):
    node_system_code = get_system_code_el(full_tree)
    node_system_code.clear()


def get_system_code_el(full_tree):
    ctr_sys_el = full_tree.getroot().find('ControlSystems').getchildren()[0]
    sys_code_el = ctr_sys_el.find('SystemCode')
    return sys_code_el

def get_controller_version(full_tree):
    ctr_sys_el = full_tree.getroot().find('ControlSystems').getchildren()[0]
    return ctr_sys_el.tag



#--- Main procedure
#--- Parsing command line input
if len(sys.argv) == 1:
    print("""\
    Usage:
         -com target_file.pdprj
         compile files in '/_source_code' directory to 'target_file.pdprj'

         -dec source_file.pdprj
         decompile code from 'target_file.pdprj' file to '/_source_code' catalog
    """)
    sys.exit(0)

if len(sys.argv) < 3:
    print("too less arguments")
    sys.exit(0)

prj_file_dir = sys.path[0]
prj_file_name = sys.argv[len(sys.argv)-1]

if not os.path.isfile(prj_file_dir + "\\" + prj_file_name):
    print("wrong file")
    sys.exit(0)

args = sys.argv[1:len(sys.argv)-1]

if "-dec" in args:
    decompile_neets(prj_file_dir, prj_file_name)
    sys.exit(0)

if "-com" in args:
    compile_neets(prj_file_dir, prj_file_name)
    sys.exit(0)
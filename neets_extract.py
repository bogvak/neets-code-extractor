from lxml import etree
import os, errno, sys

#Initial vars
initString = '<?xml version="1.0" encoding="utf-8"?>\n'
sysCodeXPath = '/Project/ControlSystems/Delta/SystemCode'

#Initial defs
def save_code_to_file(codeDir, element):
    with open(codeDir+'/'+element.tag+'.pawn', 'w') as file:
        file.write(element.text)

def decompileNeets(filePath):

    sysCodeDir = prjFileDir + "\\_system_code"

    try:
        os.makedirs(sysCodeDir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    tree = open_project_file(filePath)
    node = tree.xpath(sysCodeXPath)
    t = node[0].getchildren()
    for node in t:
        save_code_to_file(sysCodeDir, node)

def compileNeets(filePath):
    sysCodeDir = prjFileDir + "\\_system_code"
    if not os.path.exists(sysCodeDir):
        print('no System Code to compile')
        return
    filesToCompile = os.listdir(sysCodeDir)

    #clearing System Code
    tree = open_project_file(filePath)
    delete_all_elements_from_system_code(tree)

    node_system_code = tree.xpath(sysCodeXPath)

    for nextFile in filesToCompile:
        with open(sysCodeDir + '/' + nextFile) as nextFile:
            file_name, file_extension = os.path.splitext(os.path.basename(nextFile.name))
            newNode = etree.Element(file_name)
            newNode.text = nextFile.read()
            node_system_code[0].append(newNode)

    save_project_file(os.path.basename(filePath), tree)

def delete_all_elements_from_system_code(tree):
    node_system_code = tree.xpath(sysCodeXPath)
    node_system_code[0].clear()
    #t = node_system_code[0].getchildren()
    #for node in t:
     #   print(node)
      #  node.clear()

def save_project_file(file_name, tree):
    with open(prjFileDir + '/'+file_name, 'w', encoding='utf-8') as file:
        file.write(initString+etree.tostring(tree, pretty_print=True, encoding='unicode'))
    pass

def open_project_file(file_name):
    tree = etree.parse(file_name)
    return tree

#--- Main procedure
#Parsing command line input
if len(sys.argv) < 3:
    print("too less arguments")
    sys.exit(0)

if (sys.argv[1] != "-dec") and (sys.argv[1] != "-com"):
    print("no commands found")
    sys.exit(0)

prjFileDir = sys.path[0]
prjFilePath = prjFileDir + "\\" + sys.argv[2]

if not os.path.isfile(prjFilePath):
    print("wrong file")
    sys.exit(0)

if sys.argv[1] == "-dec":
    decompileNeets(prjFilePath)

if sys.argv[1] == "-com":
    compileNeets(prjFilePath)
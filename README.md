# neets-code-extractor
Simple Python-scripted command line tool to work with Neets controllers (http://www.neets.dk) project files system code parts.

### Why do we need it
We're enjoying efforts that Neets makes to provide convenient AV-controllers programming environment in the world - we're talking about Neets Project Designer software (http://www.neets.dk/products/neets-project-designer/88).
They're trying to keep amount of programming job even for complicated installation and AV projects as little as possible.

But anyway - for some project you will still need it.

But if you dealt previously with professional IDE, you probably can find that as code editor Project Designer is not the best application. So we're trying to make coding task with Project Designer a little bit easier.

After extracting code from Project Designer file you can:
- use your favorite code editor like Sublime Text;
- separate tasks - like making UI and making programming logic and do it simultaneously;
- easily copy all pieces of code from one project to other as easier as two simple commands;
- research what event handlers exist in you project - somewhere it's not that easy to do from Project Designer directly;
- keep some useful pieces of code in external files and easier include them to your project codebase;
- and so on.

### Requirements and installation
**Python**  
Installing: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
Please use latest version that includes **PIP** package manager

**lxml Python library** (http://lxml.de/)  
The easiest way to install library - using PIP manager:
```dos
X:\whatever_dir>pip install lxml
```

### Available commands
There are two possible commands so far.

**Extract code from project file**
```dos
X:\whatever_dir>python neets_extract.py -dec neets_project_file.pdprj
```
command `-dec` is shortcut to 'decompile', it will extract all code parts from **SystemCode** to `_system_code` directory.

For more details about code extracting - please refer to a wiki page [https://github.com/bogvak/neets-code-extractor/wiki/More-details-about-code-extracting].

**Compile code to project file**
```dos
X:\whatever_dir>python neets_extract.py -com neets_project_file.pdprj
```
command `-com` is shortcut to 'compile', it will automatically look for `_system_code` catalog in the same directory with project file and include all parts from this catalog to source project file.
Just to prevent corrupting of project file, script automatically back-ups original file in the same catalog with prefix _*.bk_.

**Including external pieces of code to main code files**  
You can include external pieces of code to you main code files (those are located in  `_system_code` catalog).
To do this you need to make two things.
1. You need to write following line to file where you'd like to include piece of code 
  `//|+|`**inc\lib.pawn**
  where **inc\lib.pawn** is path to file that contains your code
2. You have to add `-inc` ot your compile command.

Final command string should look like below:
```dos
X:\whatever_dir> python neets_extract.py -com -inc neets_project_file.pdprj
```

For more details about code compiling and code including - please refer to a wiki page [https://github.com/bogvak/neets-code-extractor/wiki/More-details-about-code-%22compiling%22].

# Warning!
Currently there are no additional check if code is correct or if it fits to Neets project file requirements - so it's possibly that file will be corrupted after compiling.
So if it happened - please use backed up file - it should be in the same directory, with the same filename just with '.bk' extension in the end. Back up is incremental - so you can find several backup files like '.bk1', 'bk2' and so on.

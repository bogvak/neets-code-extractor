# neets-code-extractor
Simple Python-scripted command line tool to work with Neets controllers project files code parts.

Currently only ***Delta project files*** are supported.

### Requirements
**Python**
Installing: https://www.python.org/downloads/
Please use latest version that includes **PIP** package manager

**lxml Python library** (http://lxml.de/)
The esiest way to install library - using PIP manager:
```shell
$ pip install lxml
```

### Usage
There are two possible commands so far.

**Extract code from project file**
```shell
$ python neets_extract.py -dec neets_project_source_file.pdprj
```
command `-dec` is shortcut to 'decompile', it will extract all code parts from **SystemCode** to `_system_code` directory.

**Compile code to project file**
```shell
$ python neets_extract.py -com neets_   project_source_file.pdprj
```
command `-com` is shortcut to 'decompile', it will automatically look for **SystemCode** catalog in the same directory with project file and include all parts from this catalog to cource project file.

# Warning!
Currently there are no additional check if code is correct or if it fits to Neets project file requirements - so it's possibly that file will be corrupted after compiling.
So please - **backup your project files** before compiling and use it on your own risk. 

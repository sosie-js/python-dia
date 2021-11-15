# the Mock Plugin

Goal is to simulate dia core without dia..to avoid open/close dia each time you change your python code to see the results. This can be achieved only if we have a good understanding of dia api. Making python working under Dia is not straightforward because visibility of the documentation and code sample need a deep investigation to gather the pieces of the puzzle. I have
aready generated diagram with dia python having also mocked dia-python.

Luck was Chris Daley provided with his dia-test mock project which was a complementary part I built on my side. Some parts of code I agreed, some not mainly because the api was still beta and has a lot of fake/unimplemented functions left like a bottle in the sea to find a guy that could accomplish the wow in the message bottle sent by Chris hoping someone will complete the unfinished hard work. Chris Daley explained his hard times in the article ["An easier way to write Python plugins for Dia"](https://chrisdaley.biz/easy-python-for-dia.html)

## History

- v1.0  Original version of dia-test from Chris 

- v1.1. Chris version dia-test was not fully python3 compatible so I fixed it.

- v1.2 First version with mock sample and dumpObj . 
Limitations: it can not create dia objects and dia.py is still monolitic

- v1.3 Add documentation website for pyhton-dia and this page to integrate this as the mock plugin for python dia 2.0 , 
so I changed the origin of the repos to here and mocked dia.register_action with "About DiaMock" 


## Installation 

1 - Get the mock Plugin from github

```sh
 git clone https://github.com/sosie-js/python-dia-mock-plugin) 
```

2 - Simply use my helper scripts 

```sh
source install_python2.sh
source install_python3.sh
```

they are simply calling python on setup.py to install it.

## Usage

1. copy the sample diamock.py into your dia user python dir 

2. trigger it!

either from 'dia#1' or 'dia#2' like described in the homepage of python-dia.
and watch the result in the shell console. 

OR

use Scite to trigger diamock.py

for this is updated 'python.properties' 
accessible from Menu Options > Edit Properties >  Open python.properties
by adding the command.name.2. entries and defaulting to python2.7

```
if PLAT_WIN
	command.go.*.py=pythonw -u "$(FileNameExt)"
	command.go.subsystem.*.py=1
	command.go.*.pyw=pythonw -u "$(FileNameExt)"
	command.go.subsystem.*.pyw=1
	command.build.SConscript=scons.bat --up .
	command.build.SConstruct=scons.bat .

if PLAT_GTK
	command.go.*.py=python2.7 -u "$(FileNameExt)"
	command.build.SConscript=scons --up .
	command.build.SConstruct=scons .
	command.debug.*.py=python2.7 -m pdb -u "$(FileNameExt)"
	
if PLAT_MAC
	command.go.*.py=python2.7 -u "$(FileNameExt)"
	command.build.SConscript=scons --up .
	command.build.SConstruct=scons .

command.name.1.$(file.patterns.py)=Syntax Check
command.1.$(file.patterns.py)=python -c "import py_compile; py_compile.compile(r'$(FilePath)')"
command.name.2.$(file.patterns.py)=Python3
command.2.$(file.patterns.py)=python3.9 -u  "$(FileNameExt)"
```

and watch the result in the console. 

## Contributing

Fork my repos and use instead the dev versions to develop 

```sh
source install_python2_dev.sh
source install_python3_dev.sh
```

-


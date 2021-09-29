# python-dia

A library for producing and manipulating
[Dia diagrams](http://dia-installer.de/) files.

## Demo

![Demo live](pythondia_demo.gif)

## Installation

Either can be done

-from pip (complicated with dia) 
```sh
sudo pip3 install pythondia==0.7.0
cd ~/.dia/python
unzip /usr/local/lib/python3.9/site-packages/pythondia-0.7.0-py3.9.egg 
wget  https://raw.githubusercontent.com/sosie-js/python-dia/main/tests/diapython.py
```
-from github (more straight forward = RECOMMENDED):

```sh
cd ~/.dia/python
git clone https://github.com/sosie-js/python-dia pythondia
cp pythondia/tests/diapython.py .
```

## Documents

Example python script file that can be run ONLY IN DIA

#---------- SCRIPT CANVAS ------------------

BOOT_LOADER

def dia_debug_show_diaobjs (data, flags) :

    SCRIPT

END_LOADER

dia.register_action ("DebugShowDiaObject", _("Dia _Object Factory Helper"),
                         "/DisplayMenu/Debug/DebugExtensionStart",
                         dia_debug_show_diaobjs)

#------------------------------------

where:


SCRIPT is one of the cases:

#Case 1 : Non Wrapped Objectypes in a class

```py
   
    error, dot=DiaObjectFactoryHelper("UML - Note", name="MyNote",cx=15,cy=0)
    if error  :
        errors.append(error)
    else :
        #---- Customize you dia object here:
        dot.set_property("text","Here are the two Dia Object Types created with me")
        #------
        dot.dump_properties()
        dot.add_to_layer(layer)

```

#Case 2 ; Here are some wrapped Dia Objectypes in class

```py

    db=DIA_Database_Table("Stars2",cx=10,cy=10)
    db.add_attribute("MI-6","secretAgent","JB007","License To Kill",1,0,0) 
    db.add_attribute("Office","Inspector","Columbo","License To Investigate",0,1,0) 
    db.dump_properties()
    db.add_to_layer(layer)
        
    ud=DIA_UML_Class("PyDia", cx=20,cy=10)
    ud.add_template("asterix", "le gaulois")
    ud.add_attribute("game",type="string",value="sizigi",comment="",visibility=0,abstract=0,class_scope=0)
    operation=ud.add_operation("work", "result", comment='', stereotype='', visibility=0, inheritance_type=2, query=0,class_scope=0, params=())
    operation.add_param('time', type="minutes", value="180", comment="Professional work", pindir=0)
    ud.dump_properties()
    ud.add_to_layer(layer)
```

#Case 3 : CSV

Each row follows the scheme : 
 `name , property_name(1) , property type(2); property value, property comment`

  with the first line (1) is the optional coord of the object else (0,0) and (2) is the sheet's name 

```py

   Database_Table="""
    Database - Table;(10,20);Database;;DiaObject of type "Database - Table"
    Database - Table;obj_pos;point;(14.4,10.45);
    Database - Table;obj_bb;rect;((14.4,10.45),(20.32,21.5));
    Database - Table;meta;dict;{'url': 'm_url', 'id': 'm_id', 'modification': 'm_modification', 'creation': 'm_creation', 'author': 'm_author'};
    Database - Table;elem_corner;point;(14.4,10.45);
    Database - Table;elem_width;real;5.92;
    Database - Table;elem_height;real;11.05;
    Database - Table;name;string;c_name;
    Database - Table;comment;string;c_desc;
    Database - Table;visible_comment;bool;1;
    Database - Table;underline_primary_key;bool;1;
    Database - Table;tagging_comment;bool;0;
    Database - Table;bold_primary_keys;bool;0;
    Database - Table;attributes;darray;(('a_name', 'a_type', 'a_desc', 0, 0, 0, '(NULL)'), ('', '(NULL)', 'primary', 1, 0, 0, '(NULL)'), ('(NULL)', '(NULL)', 'nullable', 0, 1, 0, '(NULL)'), ('(NULL)', '(NULL)', 'unique', 0, 0, 1, '(NULL)'), ('(NULL)', '(NULL)', 'default', 0, 0, 0, 'a_value'));
    Database - Table;normal_font;font;monospace normal normal;
    Database - Table;name_font;font;sans 700 normal;
    Database - Table;comment_font;font;sans normal italic;
    Database - Table;normal_font_height;real;0.8;
    Database - Table;name_font_height;real;0.7;
    Database - Table;comment_font_height;real;0.7;
    Database - Table;text_colour;colour;(0.0,0.0,0,0,1,0);
    Database - Table;line_colour;colour;(0.0,0.0,0.0,1.0);
    Database - Table;fill_colour;colour;(1.0,1.0,1.0,1.0);
    Database - Table;line_width;length;0.1;
    """
    ud=DIA_CSV_parser("UML - Class").parse_data(Database_Table)
    ud.dump_properties()
    ud.add_to_layer(layer)
    
    ud=DIA_CSV_parser("Database - Table").parse_data(Database_Table)
    ud.move(2.5,25)
    ud.dump_properties()
    ud.add_to_layer(layer)

```

BOOT_LOADER is at the top of your script

```py

import sys 

import logging
import gettext
_ = gettext.gettext

def install_custom_log():
    logging.basicConfig(format='{asctime}: {levelname}: {message}',
                        style='{', level=logging.DEBUG)
    logging.Formatter.default_msec_format = '%s.%03d'
    
def install_shared_module():
    with open("_once.py", 'w') as outfile:
        outfile.write("#Class holder containing imports to prevent circular imports\n")
        outfile.write("imported={}")

def check_versions() -> bool:
    from pkg_resources import get_distribution
    from platform import python_version

    failed = False

    if sys.version_info < (3, 9, 0, 'final', 0):
        logging.warning('pythonDia is not tested on Python versions prior to 3.9, but you have {} {}. Use at your own risk.'
                        .format(python_version(), sys.version_info.releaselevel))
        failed = True
        
    return failed
    
import json

import jsonpickle
from json import JSONEncoder

def json_dump(dump):
    """
        json_dump for any object, solve serializablelisable issue 
        NOTE: tuples are not handled, any invalid value cleared
        Adapted from https://pynative.com/make-python-class-json-serializable/
    """
    #Encode Object into JSON formatted Data using jsonpickle")
    dumpJSON = jsonpickle.encode(dump, unpicklable=False)
    #Ensures Json beautification will work
    obj=json.loads(dumpJSON)
    #Writing JSON Encode data into Python String")
    dumpJSONData = json.dumps(obj, indent=4)
    return dumpJSONData
    
```


END_LOADER is at the end of your script

```py


import inspect
 
install_custom_log()
 
check_versions() 

install_shared_module()
 
def onDiaLaunched():
    stack=inspect.stack()
    return ("python-startup.py" in stack[-1][1])

import _once
if __name__ == '__main__' or not onDiaLaunched():
   
    print("This free version does not have the dia core, you can only trigger from dia, sorry")

else:
    def whoami():
        stack=inspect.stack()
        return json_dump(stack[-1][1])
    
    if("dia" in globals()):
        print("DIA(G)"+__name__ )
    else:
        print("----------\nDIA"+__name__+":"+whoami()+"="+str(onDiaLaunched())+"\n----------")
        import dia
                      
    _once.imported['dia']= dia
    
    #==== SoS extension ====
    
    # Core (DON'T TOUCH THESE TWO LINES!)
    from pythonDia.objects.UML.Class import DIA_UML_Class
    from pythonDia.ObjectHelpers import DiaObjectFactoryHelper
   
    # Extras
    from pythonDia.objects.Database.Table import DIA_Database_Table
   
    # Should be the last
    from pythonDia.ObjectHelpers import DIA_CSV_parser
    
    #=================

```


## Limitations

* This free version does provide pythondia access only to objects. 
Thus, you have to use the dia api to run the meaning on each code change,
meaning you will have to close , open dia and watch errors on console to fix the 
script. Invalid scripts will not be accessible from dia app.

* For now, only objects UML Class and Database Table are supported

## Contributing

Feel free to add other object and fixes.


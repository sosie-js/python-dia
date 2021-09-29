"""
  pydia: main script - 2021.09
  ================================================
  
  Note: Experimental, will be obsolete if we found a way to use libdia /pydia libraries
  Author: SoSie@sos-productions.com
  License: LGPL
"""

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

    if sys.version_info < (3, 6, 0, 'final', 0):
        logging.warning('pythonDia is not tested on Python versions prior to 3.6, but you have {} {}. Use at your own risk.'
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
    

############ ###

def dia_debug_show_diaobjs (data, flags) :
    
    import pprint
    errors=[]

    # copied from otypes.py
    if data :
        diagram = None # we may be running w/o GUI
    else :
        diagram = dia.new("diagdebug.dia")
        data = diagram.data
    layer = data.active_layer
    
    #Case 1 : Non Wrapped Objectypes in a class_
    #------------------------------------------------------------------
   
    error, dot=DiaObjectFactoryHelper("UML - Note", name="MyNote",cx=15,cy=0)
    if error  :
        errors.append(error)
    else :
        #---- Customize you dia object here:
        dot.set_property("text","Here are the two Dia Object Types created with me")
        #------
        dot.dump_properties()
        dot.add_to_layer(layer)
        
    #Case 2 ; Here are some wrapped Dia Objectypes in class
    #--------------------------------------------------------------------------------
     
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
        
    #Case 3 : CSV
    #------------------
    
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
    
    
        
    if(len(errors) > 0):
        print("Errors encountered:\n"+"\n".join(errors))
    else:
        layer.update_extents()
        data.update_extents()
        if diagram :
            diagram.display()
            diagram.flush()
        #dot.destroy()
    return data


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
    from pythondia.objects.UML.Class import DIA_UML_Class
    from pythondia.ObjectHelpers import DiaObjectFactoryHelper
   
    # Extras
    from pythondia.objects.Database.Table import DIA_Database_Table
   
    # Should be the last
    from pythondia.ObjectHelpers import DIA_CSV_parser
    
    #=================

    dia.register_action ("DebugShowDiaObject", _("Dia _Object Factory Helper"),
                         "/DisplayMenu/Debug/DebugExtensionStart",
                         dia_debug_show_diaobjs)

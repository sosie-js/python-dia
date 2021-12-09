"""
  pydia: objects.py - 2021.11
  ================================================
  
  Advanced dia object loader ,recursive on sheets that have been saved 
  into 'objects/' directory to load shape classes defined as files.
  equivalent to:
  
  from objects import DIA_<sheet>_<object_class>
   where <sheet> is UML, Database,... as
  subdirectory of objects/ and object_class a module
   file matching objects/<sheet>/<object_class>.py
  
  Note: Experimental, will be obsolete if we found a way to use libdia /pydia libraries
  Author: SoSie@sos-productions.com
  License: LGPL
"""
#import _once
import sys
import os

dirname = os.path.dirname(__file__)

# Make a backup of sys.path
old_sys_path = sys.path[:]

#import web_pdb; web_pdb.set_trace()

## ========== Load Object Core =============== 

#from objects.UML import Class does not work in Python2
# We have to handle ourselves
#Normaly we can get the module obj directly 
#with obj=__import__('Class') but we  avoild to pollute    
sys.path.insert(0, os.path.join(dirname,"objects/UML"))
__import__('Class')  

#from Class import DIA_UML_Class
#which is equivalent to DIA_UML_Class=Class.DIA_UML_Class
#but it is more covenient to grep by names like this:
locals()["DIA_UML_Class"]  = getattr(sys.modules['Class'], "DIA_UML_Class")

#sys.path.insert(0, ".")
#from . import ObjectHelpers
try: #python2
    from ObjectHelpers import DiaObjectFactoryHelper
except:
    from pythondia.ObjectHelpers import DiaObjectFactoryHelper


## ======  Recursive class import of dia objects found in "objects/" =========

pkg_dir='objects'
classes=[]

#!NOTE : Pretty good replacement of:
#import pkgutil
#for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
#    sheet= name
#    print("Module "+name+" found in package "+pkg_dir)
for sheet in os.listdir(os.path.join(dirname,pkg_dir)):
    
    #!NOTE : Replacement candidate for importlib which does not work here, this fails:
    #import importlib
    #module=importlib.import_module('.' + name, package=pkg_dir)
    # sys.modules now holds package+'.'+name
    #ie module = sys.modules[package+'.'+name]
    #import_classes(module, locals())
    
    dir_sheet=os.path.join(dirname,"objects/"+sheet)
    sys.path.insert(0, dir_sheet)
    
    #DIA_<sheet>_<shape>=<sheet>.DIA_<sheet>_<shape>
    
    #skip file  __init__.py
    if not os.path.isdir(dir_sheet) :
        continue
            
    for file_shape in os.listdir(dir_sheet):
        if file_shape.startswith('__')  or file_shape[-3:] != '.py':
            continue
        shape=file_shape[:-3]
        
        obj=__import__(shape) #such as 'Class'

         #locals()[objname]=obj does not work in python2, we have to hook..
        # fortunately there is someone who know how to handle it
        # https://stackoverflow.com/questions/8028708/dynamically-set-local-variable
        shape_class="DIA_"+sheet+"_"+shape
        """
        code_text = shape_class+" = obj" 
        filename = ''
        code_chunk = compile( code_text, filename, 'exec' )
        exec(code_chunk) 
        """
        globals()[shape_class]  = obj
        
        """
        #print('object:DIA_'+sheet+'_'+shape)
        ###
        #!NOTE : Replaces this class importer for modules:
        def import_classes(module, vars):
            obj = module
            classes= []
            for dir_name in dir(obj):
                if dir_name.startswith('_'):
                    continue
                dir_obj = getattr(obj, dir_name)
                #print(dir_name)
                #Import the class dir_name here
                vars[dir_name]=dir_obj
        ##
        shape_class="DIA_"+sheet+"_"+shape
        locals()[shape_class]  = getattr(sys.modules[shape], shape_class)
        #print(locals()[shape_class])
        """
# Restore sys.path
sys.path[:] = old_sys_path
del old_sys_path

## ======== CSV parserFacility, should be the last ===========

try: #python2
    from ObjectHelpers import DIA_CSV_parser
except:
     from pythondia.ObjectHelpers import DIA_CSV_parser

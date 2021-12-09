import sys
import os
import inspect

# This is complicated due to the fact that __file__ is not always defined.

def GetScriptDirectory():
    
    if hasattr(GetScriptDirectory, "dir"):
        return GetScriptDirectory.dir
    module_path = ""
    try:

        # The easy way. Just use __file__.
        # Unfortunately, __file__ is not available when cx_freeze is used or in IDLE.
        if python2:
            module_path = str(os.path.abspath(inspect.getfile(GetScriptDirectory))) 
        else:
            module_path = __file__
    except NameError:
        if len(sys.argv) > 0 and len(sys.argv[0]) > 0 and os.path.isabs(sys.argv[0]):
            module_path = sys.argv[0]
        else:
            module_path = os.path.abspath(inspect.getfile(GetScriptDirectory))
            if not os.path.exists(module_path):
                # If cx_freeze is used the value of the module_path variable at this point is in the following format.
                # {PathToExeFile}\{NameOfPythonSourceFile}. This makes it necessary to strip off the file name to get the correct
                # path.
                module_path = os.path.dirname(module_path)
    GetScriptDirectory.dir = os.path.dirname(module_path)
    return GetScriptDirectory.dir

#dirname = os.path.dirname(__file__)
dirname = GetScriptDirectory()


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
        
        __import__(shape) #such as 'Class'

        #locals()[objname]=obj does not work in python2, we have to hook..
        # fortunately there is someone who know how to handle it
        # https://stackoverflow.com/questions/8028708/dynamically-set-local-variable
        shape_class="DIA_"+sheet+"_"+shape
        obj=getattr(sys.modules[shape], shape_class)
        code_text = shape_class+" = obj" 
        filename = ''
        code_chunk = compile( code_text, filename, 'exec' )
        exec(code_chunk) 
        
# Restore sys.path
sys.path[:] = old_sys_path
del old_sys_path

## ======== CSV parserFacility, should be the last ===========

try: #python2
    from ObjectHelpers import DIA_CSV_parser
except:
     from pythondia.ObjectHelpers import DIA_CSV_parser


del GetScriptDirectory,inspect, ObjectHelpers, classes, dir_sheet, dirname, file_shape, obj, os, pkg_dir, shape, shape_class, sheet, sys
"""
  pydia: Class.py - 2021.09
  ================================================

  Sheet: UML
  Note: Experimental, will be obsolete if we found a way to use libdia /pydia libraries
  Author: SoSie@sos-productions.com
  License: LGPL
"""


import _once
_once.imported['DIA_UML_Class']= None
if not 'DiaObjectFactoryHelper' in _once.imported.keys() :
    import sys
    python2 = (sys.version_info[0] == 2)
    if python2:
        import os
        dirname = os.path.dirname(__file__)
        sys.path.insert(0, os.path.join(dirname,"../.."))
        from ObjectHelpers import DiaObjectFactoryHelper
    else:
        from pythondia.ObjectHelpers import DiaObjectFactoryHelper

class UML_ClassOperationParamHelper:

    def __init__(self, name, type, value, comment="", pindir=0):
    #===================================    
        self.name=name # name : str = "name for this param"
        self.type=type #  type : str = "type of this param"   
        self.value=value # str = "default value for this param"
        self.comment=comment # comment : str = "comment for this param"
        self.pindir=pindir # pin direction int  = 0-3

    def flush_changes(self):
    #--------------------------------
        param=(tuple([self.name, self.type, self.value, self.comment, self.pindir]),)
        return param
    
class UML_ClassOperationHelper:

    def __init__(self,name, type, comment='', stereotype='', visibility=0, inheritance_type=2, query=0,class_scope=0):
        self.name=name
        self.type=type
        self.comment=comment
        self.stereotype=stereotype
        self.visibility=visibility
        self.inheritance_type=inheritance_type
        self.query=query
        self.class_scope= class_scope
        self.params=[]
    
    def add_param(self, name, type="", value="", comment="", pindir=0):
    #--------------------------------------------------------------------------------------------------------------
        self.params.append(UML_ClassOperationParamHelper(name, type, value, comment, pindir))
    
    def flush_changes(self):
    #------------------------------
        params=()
        for param in self.params:
            params= params + param.flush_changes()
        operation=(tuple([self.name, self.type, self.comment, self.stereotype, self.visibility, self.inheritance_type, self.query,self.class_scope, params]),)
        return operation
        
class UML_ClassAttributeHelper:

    def __init__(self,name,type="",value="",comment="",visibility=0,abstract=0,class_scope=0):
        self.name=name
        self.type=type
        self.value=value
        self.comment=comment
        self.visibility=visibility
        self.abstract=abstract
        self.class_scope=class_scope
    
    def flush_changes(self):
    #------------------------------
        attribute=(tuple([self.name,self.type,self.value,self.comment,self.visibility,self.abstract,self.class_scope]),)
        return attribute

class UML_ClassTemplateHelper:

    def __init__(self,name,type=""):
        self.name=name
        self.type=type
    
    def flush_changes(self):
    #------------------------------
        template=(tuple([self.name,self.type]),)
        return template
    
 
class DIA_UML_Class():
        
    def __init__(self,name="",cx=0, cy=0):
    #========================
        error, dot=DiaObjectFactoryHelper("UML - Class", name=name, cx=cx, cy=cy)
        self.error=error
        self.dot=dot
            
    def add_template(self,name, type):
    #-----------------------------------------------------
        """
        add a template 
        """
        template=UML_ClassTemplateHelper(name,type)
        self.dot.templates.append(template)
        return template
    
    def add_attribute(self,name,type="",value="",comment="",visibility=0,abstract=0,class_scope=0):
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
        """
        add an UML Attribute
        """
        attribute=UML_ClassAttributeHelper(name,type=type,value=value,comment=comment,visibility=visibility,abstract=abstract,class_scope=class_scope)
        self.dot.attributes.append(attribute)
        return attribute
    
        
    def add_operation(self,name, type, comment='', stereotype='', visibility=0, inheritance_type=2, query=0,class_scope=0, params=()):
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------   
        """
        add an UML operation
        """
        operation=UML_ClassOperationHelper(name, type, comment=comment, stereotype=stereotype, visibility=visibility, inheritance_type=inheritance_type, query=query,class_scope=class_scope)
        self.dot.operations.append(operation)
        return operation
    
    @classmethod
    def  handler(self,cls,row): #NOTE: cls is DIA_CSV_parser 
    #-----------------------------------    
        (c_name,p_name,p_type,p_value,p_desc) = row
        #print(row)
        if(p_name =="" or p_name[0] =="("): #Create the UML class
          
            if(p_name ==""):
                pos="(0,0)"
            else :
                pos=p_name

            #Extract cs, cy from the coordinate recipe
            import re
            [cx, cy]=[t(s) for t,s in zip((float,float),re.search('^\(([-+]?\d*\.\d+|\d+),([-+]?\d*\.\d+|\d+)\)$',pos).groups())]
            #print("Decoded:",cx,cy)
            c_name=c_name.strip()
            c_desc=p_desc.strip()
            c_stereotype=""
            dtype=DIA_UML_Class(c_name, cx=cx,cy=cy) 
            error=dtype.error 
            dot= dtype.dot
            if error  :
                errors.append(error)
            else :
                dot.set_property("comment",c_desc)
                dot.set_property("stereotype",c_stereotype)
                cls.objects["O"+str(len(cls.objects)+1)] = dtype
        else:
            to=c_name.strip()   
            a_name=p_name.strip()
            a_type=p_type.strip()
            a_value=p_value.strip()
            a_comment=p_desc.strip()
            a_visibility=0
            a_abstract=0
            a_class_scope=0
            
            if( "(" in p_name):
                #decode params
                
                cls.last_object().add_operation(a_name, a_type, comment=a_comment, stereotype='', visibility=0, inheritance_type=2, query=0,class_scope=0, params=())
            else: #append the attribute
                cls.last_object().add_attribute(a_name,type=a_type,value=a_value,comment=a_comment,visibility=a_visibility,abstract=a_abstract,class_scope=a_class_scope)
        
        
    def flush_changes(self) :
    #-------------------------------
        self.dot.flush_changes()
    
    def add_to_layer(self,layer):
    #-----------------------------------
        self.flush_changes()
        self.dot.add_to_layer(layer)
        
    def dump_properties(self):
    #----------------------------------
        self.dot.dump_properties()  
 

_once.imported['DIA_UML_Class']= DIA_UML_Class
        
for name, object in _once.imported.items():
    globals()[name]=object
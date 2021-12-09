"""
  pydia: Table.py - 2021.11
  ================================================

  Sheet: Database
  Note: Experimental, will be obsolete if we found a way to use libdia /pydia libraries
  Author: SoSie@sos-productions.com
  License: LGPL
"""


import _once
_once.imported['DIA_Database_Table']= None
if not 'DiaObjectFactoryHelper' in _once.imported.keys() :
    from ObjectHelpers import DiaObjectFactoryHelper

 
class Database_TableAttributeHelper:

    def __init__(self,name,type,value,comment="",primary=0,nullable=0,unique=0):
    #===================================================
        self.name=name
        self.type=type
        self.value=value
        self.comment=comment
        self.primary=primary
        self.nullable=nullable
        self.unique=unique
    
    def flush_changes(self):
    #------------------------------
        attribute=(tuple([self.name, self.type, self.comment, self.primary, self.nullable, self.unique, self.value]),)
        return attribute
        

class DIA_Database_Table():
        
    def __init__(self,name="",cx=0, cy=0):
    #========================
        error, dot=DiaObjectFactoryHelper("Database - Table", name=name, cx=cx, cy=cy)
        self.error=error
        self.dot=dot
        print(error)
        
    def add_attribute(self,name,type,value,comment="",primary=0,nullable=0,unique=0) :
    #------------------------------------------------------------------------------------------------------------------------------------
        a_name=''
        if(name!=""):
            a_name=name
        a_type=''
        if(type!=""):
            a_type=type
        a_comment=''
        if(comment!=""):
            a_comment=comment 
        a_primary=0
        if(primary) :
            a_primary= primary
        a_nullable=0    
        if(nullable) : 
            a_nullable= nullable        
        a_unique=0
        if(unique) :
            a_unique = unique        
        a_default=''
        if(value) : 
            a_default=value
        
        attribute=Database_TableAttributeHelper(a_name, a_type,a_default,comment=a_comment, primary=a_primary,nullable=a_nullable,unique=a_unique)


        self.dot.attributes.append(attribute)
        return attribute
        
    @classmethod
    def  handler(self,cls,row): #NOTE: cls is DIA_CSV_parser after relocation
    #-----------------------------------    
        import re
        (c_name,p_name,p_type,p_value,p_desc) = row
        #print(row)
        if(p_name =="" or p_name[0] =="("): #Create the database table 
          
            if(p_name ==""):
                pos="(0,0)"
            else :
                pos=p_name

            #Extract cs, cy from the coordinate recipe
            [cx, cy]=[t(s) for t,s in zip((float,float),re.search('^\(([-+]?\d*\.\d+|\d+),([-+]?\d*\.\d+|\d+)\)$',pos).groups())]
            #print("Decoded:",cx,cy)
            c_name=c_name.strip()
            c_desc=p_desc.strip()
            c_stereotype=""
            dtype=DIA_Database_Table(c_name, cx=cx,cy=cy) 
            error=dtype.error 
            dot= dtype.dot
            if error  :
                errors.append(error)
            else :
                dot.set_property("comment",c_desc)
                cls.objects["O"+str(len(cls.objects)+1)] = dtype
        else:
            to=c_name.strip()   
            a_name=p_name.strip()
            a_type=p_type.strip()
            a_value=p_value.strip()
            a_comment=p_desc.strip()
            
            if(a_name== "attributes"):
                if(a_value == "()"):
                    pass
                else :
                    from ast import literal_eval
                    try:
                        attributes = literal_eval(a_value )
                        for attribute in attributes :
                            # regexp='\((\s*),(\s*),(\s*),(\d),(\d),(\d),(\s*)\)'
                            #[name, type, comment, primary, nullable, unique, value]=[t(s) for t,s in zip((str,str, str,int,int, int, str),re.search(regexp,a_value).groups())]
                            [name, type, comment, primary, nullable, unique, value]=attribute
                            cls.last_object().add_attribute(name,type,value,comment=comment,primary=primary,nullable=nullable,unique=unique) 
                    except BaseException as e:
                        print("Cannot match Regexp "+regexp)
                        print("on value: "+a_value)
                        raise(e)
                   
            else:
                cls.last_object().set_property(a_name,a_value, a_type)
   

    def set_property(self, name, value, type=''):
    #------------------------------------------------------
        self.dot.set_property(name, value, type)

    def get_property(self, name):
    #-------------------------------------------
        return self.dot.get_property(name)
                
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
     

_once.imported['DIA_Database_Table']= DIA_Database_Table
        
for name, object in _once.imported.items():
    globals()[name]=object
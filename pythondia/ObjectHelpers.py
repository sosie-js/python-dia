

import _once
_once.imported['DiaObjectFactoryHelper']= None
import pprint
import inspect


def dia_debug_props_cb_as_csv (data, flags) :
    for layer in data.layers :
        print("Layer :", layer.name)
        for o in layer.objects :
            otype=o.type.name
            print('DiaObject of type "'+otype+'"')
            c_name=otype
            props = o.properties
            for s in list(props.keys()) :
                p_name=s 
                p_type=props[s].type 
                #" (visible=%d)" % props[s].visible)
                try :
                    p = props[s].value
                except :
                    p = None
                p_value=str(p)
                p_desc=""
                print(c_name+";"+p_name+";"+p_type+";"+p_value+";"+p_desc)
             
#from allsheets.py

# Given a list of "sheet objects" return the common namespace of the object types
def so_get_namespace (sol) :
	names = {}
	if len(sol) < 1 :
		return "Empty"
	for ot, descr, fname in sol :
		if ot :
			sp = ot.name.split(" - ")
			if len(sp) > 1 :
				if sp[0] in names:
					names[sp[0]] += 1
				else :
					names[sp[0]] = 1
	return ",".join (list(names.keys()))

def check_objecttype_overlap (sheets) :
	types = dia.registered_types()
	# remove Standard objects, they do not have or need a sheet
	del types["Group"]
	for s in ["Arc", "Box", "BezierLine", "Beziergon", "Ellipse", "Image", "Line",
		  "Outline", "Path", "Polygon", "PolyLine", "Text", "ZigZagLine"] :
		del types["Standard - %s" % (s,)]
	# got through all the sheets to match against registered types
	missing = []
	for sheet in sheets:
		for ot, descr, fname in sheet.objects:
			if ot.name in types:
				if ot == types[ot.name]:
					del types[ot.name]
				else:
					print("Mix-up:", ot.name)
			else:
				# sheet referencing a type not available
				missing.append(ot.name)
	# from the dictionary removed every type referenced just once?
	print(types)

def packagesheets():
    sheets = dia.registered_sheets()
    check_objecttype_overlap (sheets)
    for sheet in sheets :
        info = "Namespace: [%s]<br>%i object types" % (so_get_namespace (sheet.objects), len(sheet.objects))
        sname = sheet.name
        if not sheet.user :
            sname = "*" + sname + "*"
        print ("%s;%s;%s" % (sname, sheet.description, info))
        
        
def get_packagesdict(keys):
    #build the packages list with their component
    packages = {}
    for s in keys :
        kt = s.split(" - ")
        if len(kt) == 2 :
            if len(kt[0]) == 0 :
                sp = "<unnamed>"
            else :
                sp = kt[0]
            st = kt[1]
        else :
            sp = "<broken>"
            st = kt[0]
        if sp in packages :
            packages[sp].append(st)
        else :
            packages[sp] = [st] 
    return packages

#============================================

import json

import jsonpickle
from json import JSONEncoder

def json_dump(dump):
    """ 
        json_dump for any object, solve serializablelisable issue 
        Adapted from https://pynative.com/make-python-class-json-serializable/
    """
    #Encode Object into JSON formatted Data using jsonpickle")
    dumpJSON = jsonpickle.encode(dump, unpicklable=False)
    #Ensures Json beautification will work
    obj=json.loads(dumpJSON)
    #Writing JSON Encode data into Python String")
    dumpJSONData = json.dumps(obj, indent=4)
    return dumpJSONData

class DiaObjectypeHelper:

    def append_attribute_def(self,pp):
    #-----------------------------------------------------
        o_real =self.object
       
        p_name=pp
        p_type=o_real.properties[pp].type
        try :
            p = o_real.properties[pp].value
        except :
            p = None
        p_value=str(p)
        #" (visible=%d)" % o_real.properties[pp].visible)
        self.attrs.append((p_name, p_type, p_value))

    def __init__(self,st,name="",cx=0, cy=0):
    #=========================
     
        self.st= st
        self.name = name
        self.pool_to_flush = [] 
        otypes = dia.registered_types()
  
        if st in otypes: # otypes.has_key(st) :
            o_real, h5, h6 = dia.get_object_type(st).create(cx,cy)
        else :
            o_real = None
            print("Failed to create object", sp, st)
            raise("stop in DiaObjectypeHelper")
            
        self.object=o_real
    
        if not o_real is None :
            for p in o_real.properties.keys() :
                #print(o_real)
                #print(o_real.properties)
                #print(p, o_real.properties[p])
                
                #For attributes,... 
                if o_real.properties[p].type == 'darray' :  
                    self.pool_to_flush.append(p)
                    values=o_real.properties[p].value
                    if(isinstance(values,str)) :
                        if(values != "()"):
                            raise(Exception("Unsupported: Default value is not empty for "+p+ " "+str(o_real.properties[p].value)))
                    elif(len(values)): #tupple
                        raise(Exception("Unsupported: Default value is not empty for "+p+ " "+str(o_real.properties[p].value)))
                    setattr(self, p, [])       

            if(name == ""):
                name=st
            if o_real.properties.has_key("name") :
                 self.set_property("name", name)
                 1
            self.handles=(tuple([h5,h6]),)
        
    def dump_properties(self):
        
        self.flush_changes()
        
        #dot.object.parent return None, it's buggy imho
        #fortunately we backup it in st
        
        print("### "+self.st +":"+self.name)
        print("###########################")
        for key in self.object.properties.keys():
            property=self.object.properties[key]
            if  property.type == "darray" and len(property.value) > 1 :
                print("%s:%s=" % (property.name, property.type))
                pprint.pprint(property.value)
            else:
                print("%s:%s=%s" % (property.name, property.type, str(property.value)))
                
    def flush_changes(self):
        """
        if(self.st == "Database - Table"):        
            self.object.properties["attributes"]=self.attributes 
            
        if(self.st == "UML - Class"):       
            self.object.properties["templates"]=self.templates
            self.object.properties["attributes"]=self.attributes
            self.object.properties["operations"]=self.operations
            
        ...
        """
        props=self.pool_to_flush
        for prop in props:
            #print("Flushing property "+prop)
            attr_flush=()
            for attr in getattr(self, prop):
                attr_flush= attr_flush+attr.flush_changes()
            self.set_property(prop, attr_flush)
            
    def set_property(self, name, value, ptype=""):
    #---------------------------------------------------------------------
        from ast import literal_eval
        if(ptype != "" and ptype !="string"):
            if isinstance(value, str): 
                #parse string safely for int, tuples, bool...
                try:
                    pvalue=literal_eval(value )
                except SyntaxError:
                    pvalue = value
            else:
                pvalue=value
        else:
            pvalue=value
       
        if(name == "obj_pos"):
            #print('set_property: Use move(x,y) instead'
            x=pvalue[0]
            y=pvalue[1]
            self.move(x, y)
        else:
            try:
                self.object.properties[name].value=pvalue
            except: #dia text handling is special .value.text is read-only
                try:
                    self.object.properties[name]=pvalue
                except:
                    read_only_props=["obj_pos","obj_bb"]
                    if(name in read_only_props):
                        print("Failed to set READ-ONLY property "+ptype+" "+name)
                    else:
                        print("Failed to set_property "+ptype+" "+name+" to "+str(type(value))+" = "+str(value) + ", prop may be READONLY?")
                    
    def get_property(self, name):
        return self.object.properties[name].value
     
    def move(self, x, y):
        return self.object.move(x,y)
     
    def add_to_layer(self, layer):
        layer.add_object(self.object)
    
    def destroy(self):
        if not self.object is None :
            self.object.destroy()
            del self.object


def DiaObjectFactoryHelper(typename="",name="",cx=0, cy=0)  :  # ->  (str, DiaObjectypeHelper)
#---------------------------------------------------------------------------------------------------------------------------------------------------

    otypes = dia.registered_types()
    keys = otypes.keys()
    sorted(keys)
    packages=get_packagesdict(keys)
    error=""
    dot=None
    
    if typename=="" :
        error="dia_debug_show_diaobjs ended."
        print(str(len(packages))+" Dia Object Packages Available")
        for packagename, otypenames in packages.items():
             print("["+packagename+"]:"+",".join(otypenames))
    else:

        if " - " in typename : 
            if typename in keys:
                #print("Found")
                otname=typename
               
                try:
                    dot=DiaObjectypeHelper(otname, name=name,cx=cx, cy=cy)
                except Exception as e:
                    raise(e)
                    error="Failed to create object type "+otname + ", reason was "+str(e)
                    
                return error, dot
 
            #------------------------------
        kt = typename.split(" - ")
        if len(kt) == 2 :
            if len(kt[0]) == 0 :
                sp = "<unnamed>"
            else :
                sp = kt[0]
            st = kt[1]
        else :
            sp = "<broken>"
            st = kt[0]
        if sp ==  "<broken>" and st not in packages["<broken>"]:
            error="Unsupported Dia Object type '"+typename+"', please prepend package name <pname> with '<pname> - '"
        else:
            if sp in packages :
                if not st in packages:
                     error="Sorry the object type '"+st+"' was not found in the package '"+sp+"', available types are "+",".join(packages[sp])
            else:
                error="Unsupported Dia Package '"+sp+'"'
        
    return error, dot
    
_once.imported['DiaObjectFactoryHelper']= DiaObjectFactoryHelper

class DIA_CSV_parser:
    
    def last_object(self):
    #--------------------------------
        return self.objects["O"+str(len(self.objects))]
  
    def __init__(self, target="UML - Class"):
    #------------------------------------------------------------------    
        self.target=target
        self.objects={}
            
    def parse_stream(self,stream):
    #--------------------------------------------------------- 
        import csv
        count = -1 
        createdCards = 0
        skip_header= False
        import sys
        try:
            cname="DIA_"+self.target.replace(" - ","_")
            klass=_once.imported[cname]#globals()[cname]
            handler=klass.handler
        except BaseException as e:
            raise(Exception("DIA_CSV_parser: No handler for "+cname+", error was "+str(e)))

        with stream as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                count += 1
                if count == 0 and skip_header:
                    print("skipping file header: " + str(row) + "\n")
                    continue
                #if row[0] == '' and row[1] == '':
                #    print("skipping empty row (count = {})".format(count))
                #    continue
                if(len(row) > 1): #1 to avoid spaced or empty lines
                    try:
                        handler(self,row)
                    except BaseException as e:
                        print(row)
                        raise(e)

    def parse_data(self,data):
    #---------------------------------------------------------   
        import io
        stream = io.StringIO(data)
        self.parse_stream(stream)
        return self
    
    def parse_file(self, csvPath):
    #---------------------------------------------------------
        import os
        if not os.path.isfile(csvPath):
                raise("csvPath doesn't exist: '{}'".format(csvPath))

        print("reading csv: '{}'\n".format(csvPath))
        stream = open(csvPath, newline='')
        self.parse_stream(stream)
        return self
    
    def set_property(self, name,value):
    #---------------------
        self.last_object().dot.set_property(name,value)
        
    def move(self, x,y):
    #---------------------
        self.last_object().dot.move(x,y)
        
    def flush_changes(self) :
    #-------------------------------
        for dtype in self.objects.values():
            dot=dtype.dot
            dot.flush_changes()
    
    def add_to_layer(self,layer):
    #-----------------------------------
        self.flush_changes()
        for dtype in self.objects.values():
            dot=dtype.dot
            dot.add_to_layer(layer)
        
    def dump_properties(self):
    #----------------------------------
        for dtype in self.objects.values():
            dot=dtype.dot
            dot.dump_properties()   
            
_once.imported['DIA_CSV_parser']= DIA_CSV_parser

for name, object in _once.imported.items():
    globals()[name]=object
    
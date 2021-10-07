# Copyright 2021 SoSie - sos-productions.com
#
#   diaconnect.py ..  make dia awesome with python from outside (V2 - Uggly refresh hack)
#   
# Warning: 
#  this version is *beta*, with no warranty and security so don't use it for production unless you know the risks
#  of telnet without pasword
#
# Big thanks to:
#  -Dia authors
#  -Hans Breuer for bringing python samples and codes to the surface
#  -Zander brown who takes the time to maintains Dia
#  -dia contributors and many others in the dia mailing list such as Chris Daley (I will merge his dia mock with mine)...
#  -https://tenthousandmeters.com/blog/python-behind-the-scenes-13-the-gil-and-its-effects-on-python-multithreading/
#
# Requirements:
#  -pythondia, see installation steps on github.com/sosie-js/python-dia
#
# Usage:
# -trigger dia like this: "dia&&source finish_tour.sh&&rm finish_tour.sh"
# -telnet locally with " telnet 127.0.0.1 33333" then try one command to see what happen in dia such as ok, ko1, ko2 [enter]
#
# Wants more?
# -watch the awarded films after injecting buttons on sosie.sos-production.com, 
# - sign petition endccp.com to help people of china , hk and the world to end this biological attack from Wuhan. 
#   the journalist Jean Robin explained with proofs on his website https://nouvellefrancelibre.com/in-english/.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


def dia_run_pythondia(data, flags):
    """ will hold the python script wrapped for dia connect , I don't know how to make this dynamic, live edit unless convert all commands to CSV all load the CSV file.."""

    import _once
    layer = data.active_layer
    
    import pythondia
    
    #==== SoS extension ====
    
    # Core (DON'T TOUCH THESE TWO LINES!)
    from pythondia.objects.UML.Class import DIA_UML_Class
    from pythondia.ObjectHelpers import DiaObjectFactoryHelper
   
    # Extras
    from pythondia.objects.Database.Table import DIA_Database_Table
   
    # Should be the last
    from pythondia.ObjectHelpers import DIA_CSV_parser
    
    #display = dia.active_display() returns None, so we have to rely on our backuped diagram
    diagram=_once.diagram
    
    #from pudb import set_trace; set_trace(paused=True)
    #import web_pdb; web_pdb.set_trace()
    if(diagram):
        
        #========== PUT YOUR PYDIA SCRIPT HERE ===========
        
        otypes=dia.registered_types() 
        print(otypes) #BUG1: Shows only AADL Sheet ! Others like UML are not present
        
        errors=[]
        
        #Case 1 : Non Wrapped Objectypes in a class_
        #------------------------------------------------------------------
        error, dot=DiaObjectFactoryHelper("UML - Note", name="MyNote",cx=15,cy=0)
        if error  :
            errors.append(error)
        else :
            #---- Customize you dia object here:
            dot.set_property("text","Created with pythondia!")
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
            
        ud=DIA_UML_Class("PyDiaMe", cx=20,cy=10)
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
        
        #========================================
        
        if(len(errors) > 0):
            print("Errors encountered:\n"+"\n".join(errors)) # BUG1 leads to Unsupported Dia Package 'UML"
        else:
     
            """
            if diagram :
                diagram.display()
                diagram.flush()
                print("FLUSH")
                print(str(dia))
                print(str(d))
                #display_refresh(dia)
            """
            # NOTE: Extracted from the Blink example in Dia Mailing list May 2009 
            #found by chance thanks to DocFetcher tool..using 'script' keyword
            # I don't know if we need this...display_refresh() may be called simply directly
            from gi.repository import GObject as gobject
            gobject.timeout_add(500, display_refresh)
            
            target=str(diagram.data)
            #NOT CHANGING the target is crashing DIA, target=target.replace(".dia","_foo.dia")
            print("saving diagram into '"+ target+"'")
            diagram.save ( target)
            
            #THIS REALLY SUCKS AND DO NOTHING!
            #dia.load(target)
            #dia.update_all()
            #WE HAVE TO USE THE MACGYVER MODE
            import subprocess
            p=subprocess.Popen(["dia", target])
            print(p.pid)
            #dia.flush()
            #animator.start()
    else:
        print("Diaconnect requires first you click on the entry 'diaconnect' from Debug menu of dia")
    #return data

def handle_client(sock): 
    """ handles commands of Dia connect server, please adjust ot your needs it's free """
 
    #timer = RepeatTimer(5, beegees, "Oh oh oh staying alive...")
    #timer.start()             
    while True:
        received_data = sock.recv(4096)
        if not received_data:
            break
        command = received_data.decode('utf-8').rstrip()
                  
        state="received"
        if(command == 'ok'):
            import _once
            diagram=_once.diagram
            data=dia_run_pythondia(diagram.data, None)            
        elif(command == 'ko1'):
            crash_dia(1)
        elif(command == 'ko2'):
            crash_dia(2)
        else:
            state="INVALID"
            
        #just an echo so we know server received correctly the command  
        print(state+" COMMAND "+command)
        sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


#######################################################################
###   DIA CONNECT  FOR THE UGLY DIA THAT DOES NOT WANT TO REFRESH SCREEN AND SANDBOXED LIKE HELL ###
#######################################################################

import inspect
 
def onDiaLaunched():
    """ Detect if this python script is run within dia, if it is is the case return True"""
    stack=inspect.stack()
    return ("python-startup.py" in stack[-1][1])

if __name__ == '__main__' or not onDiaLaunched():

    print("Nothingto do, copy this script in ~/.dia/python , then open dia with : dia&&source finish_tour.sh")

else:
    
    import dia
    
    def install_shared_module():
        """ Create the _once.py that will serve as a shared memory between modules"""
        with open("_once.py", 'w') as outfile:
            outfile.write("#Class holder containing imports to prevent circular imports\n")
            outfile.write("imported={}\n")
            outfile.write("diagram=None")

    install_shared_module()

    #
    # DIA CONNECT CLIENT (Telnet or DIA ACTION)
    #

    def send_diaconnect_command(cmd):
        """Contact diaconnect server and send a command"""
        import sys
        import telnetlib

        tn = telnetlib.Telnet("127.0.0.1","33333")
        tn.read_until(b"Escape character is '^]'.", 2)
        tn.write(cmd.encode('utf-8')+b"\n")
        tn.close
    
    def diaconnect_run(diagram,b):
        send_diaconnect_command("ok")
        return b
        
    dia.register_action ("DiaConnect", "Dia Connect", 
                         "/DisplayMenu/Debug/DebugExtensionStart", 
                         diaconnect_run)


    #
    # DIA CONNECT SERVER
    #

    def run_server():
        """ Run the server but save the pid in the shell script so we will be able to kill it without the killall dia shell command"""  
        import os
        #save the pid so you will be able to kill the process when parent dia is closed with source finish_tour.sh
        with open("finish_tour.sh", 'w') as outfile:
                outfile.write("#!/usr/bin\n")
                outfile.write("kill -9 "+str(os.getpid()) )

        run_web_server()


    from threading import Thread, Timer

    class RepeatTimer(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)

    class OnceTimer(Timer):
        def run(self):
             if self.finished.wait(self.interval):
                print('repeat one '+str(self.interval))
                self.function(*self.args, **self.kwargs)

    import socket

    def run_web_server(host='127.0.0.1', port=33333):
        """ Create a telnet socket for the dia connect server"""
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen()
        print("Dia connect Server on "+host+" started, listening on port "+str(port))
        while True:
            client_sock, addr = sock.accept()
            print('Connection from', addr)
            Thread(target=handle_client, args=(client_sock,)).start()

    """
    MAYDAY! crashes dia, related with https://stackoverflow.com/questions/18647475/threading-problems-with-gtk
    introducing XinitThreads like suggested in app/dia-prop.c (see  https://github.com/sosie-js/dia/tree/pythondia-crash) 
    """
    def crash_dia(method):
        if(method == 1) :
            dia.message(2, "Hello, World!") 
        else :
            import gi
            gi.require_version("Gtk", "2.0")
            from gi.repository import Gtk

            window = Gtk.Window(title="Hello World")
            window.show()
            window.connect("destroy", Gtk.main_quit)
            Gtk.main()
            
    _diagram=None

    #SUCKS AND CRASH
    def display_refresh():
        import _once
        dia=_once.imported['dia'] 
        active_display=dia.active_display()
        diagram=active_display.diagram
        data = diagram.data
        layer = data.active_layer
        #objects = layer.objects
        layer.update_extents()
        data.update_extents()
        dia.update_all()
        dia.flush()
        return 0
        
    server_started=False
    import multiprocessing as mp
    
    def thread_server():
        """ Don't now if we really need this encapsulation but it works"""
        global server_started
        if not  server_started:
            server_started=True
            thr = mp.Process(target=run_server)
            #thr.daemon=True
            thr.start ()
        return 1

    autolaunch=False
    
    def autolaunch_server():
        """ Dia Connect server is started as a daemon when dia is launched"""
        global autolaunch
        import _once
        
        if not autolaunch :
            active_display=dia.active_display()
            diagram=active_display.diagram
            globals()["_diagram"]=diagram
            _once.diagram=diagram
            _once.imported['dia']=dia
            #dia.message(2,"Diaconnect is ready now, pass your commands through telnet localhost 127.0.0.1 33333:")
            #try:
            #   import gobject
            #except importError as e:
            #    from pudb import set_trace; set_trace(paused=True)
            from gi.repository import GObject as gobject
            gobject.timeout_add(1000, thread_server)
            
            autolaunch= True
            
        return 1 #Daemon mode
        
    from gi.repository import GObject as gobject
    gobject.timeout_add(1000, autolaunch_server)
    
# Copyright 2021 SoSie - sos-productions.com
#
#   diagtkbuilder.py ..  experinenting timer and gui with hello world sample both inside and outside dia
#
# Requires diagtkbuilder.glade
# (use Glade 3.8.0 and export to gtkbuilder format to customize your gui):
"""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk+" version="2.24"/>
  <!-- interface-naming-policy toplevel-contextual -->
  <object class="GtkWindow" id="window1">
    <property name="can_focus">False</property>
    <child>
      <object class="GtkButton" id="button1">
        <property name="label" translatable="yes">button</property>
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <property name="receives_default">True</property>
        <property name="use_action_appearance">False</property>
      </object>
    </child>
  </object>
</interface>
"""
# for info, diagtkbuilder3.glade is quite similar:
"""
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.22.1 -->
<interface>
  <requires lib="gtk+" version="3.20"/>
  <object class="GtkWindow" id="window1">
    <property name="can_focus">False</property>
    <child>
      <placeholder/>
    </child>
    <child>
      <object class="GtkButton" id="button1">
        <property name="label" translatable="yes">button</property>
        <property name="visible">True</property>
        <property name="can_focus">True</property>
        <property name="receives_default">True</property>
      </object>
    </child>
  </object>
</interface>
"""
# License:
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


from threading import Timer, Thread, Event
#from threading import _sleep does not exist in python3 threading
#Use this: 
"""
def sleep_timeout(t=0):
    if(t) :
        timer = OnceTimer(t, sleep_timeout)
        timer.start() 
        timer.join()
"""
 
#import sys
#print(sys.builtin_module_names)

class RepeatTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()



class OnceTimer():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def cancel(self):
        self.thread.cancel()


import sys
python2 = (sys.version_info[0] == 2)

#NOTE, As Namespace Gtk is already loaded with version 2.0, 
#for dia 0.97.2, we cannot choose 3.0
if(python2) :
    gtk_ver= '2.0' #PyGTK outdated
    gtk_ver= '2.0gi' #or pygobject
else: #python3
    gtk_ver= '2.0gi'
    #gtk_ver= '3.0gi' Not yet compatible with dia see https://gitlab.gnome.org/GNOME/dia/-/issues/408
 
#deduced from gtkcons.py
if(gtk_ver== '2.0'):
    #PyGTK is the recomended python module to use with Gtk 2.0
    import pygtk
    pygtk.require('2.0')

    #Because Gtk 2.0 was not designed for use with introspection some of the interfaces 
    #and API will fail.  As such this is not supported by the pygobject development team 
    #and we encourage you to port your app to Gtk 3 or greater. 
    import gtk
    import gtk.keysyms
    import gobject
elif("gi" in gtk_ver) :
    import gi
    gtk_ver=gtk_ver.replace("gi","")
    gi.require_version('Pango', '1.0')
    gi.require_version('Gtk', gtk_ver)
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        from gi.repository import GObject as _gobject , Pango, Gtk as gtk, Gdk
        from gi.repository import GLib as gobject #PyGIDeprecationWarning: GObject.timeout_add is deprecated; use GLib.timeout_add instead

autolaunch=False
    
def autolaunch_server(data, flags):
    """ Dia Connect server is started as a daemon when dia is launched"""
    global autolaunch
    
    if not autolaunch :

        autolaunch= True
        
        #Old pygtk way for Glade:
        #import gtk.glade
        #xml = gtk.glade.XML('project1.glade')
        
        #Use the tool gtk-builder-convert to convert glade2 to gtkbuilder (glade3, root node is interface):   
        # gtk-builder-convert project1.glade project1_gtkbuikder.glade
        # as mentioned in https://lists.debian.org/debian-gtk-gnome/2012/02/msg00003.html
        builder = gtk.Builder()
        builder.add_from_file('diagtkbuilder.glade') #from-glade3.8.0 , gtk+2.0 compatible
        #builder.add_from_file('diagtkbuilder3.glade') #from glade 3.22.1 , gtk3.0 compatible
         
        #window = xml.get_widget('window1')
        window = builder.get_object("window1")
        
        #window.connect("delete_event", gtk.main_quit)
        window.connect('delete-event', gtk.main_quit)

        #button = xml.get_widget('button1')
        button = builder.get_object("button1")
        
        button .connect("clicked", on_button_clicked)
        
        window.show_all()
        gtk.main()
        
    return 1 #repeat


def greeting():
    import sys
    print("Hello You") #unbuffered script, started with  python3 -u hello_gtkbuilder.py
    sys.stdout.flush() #python2

def _repeat(a):
    return a() # Let the process decide if we keep alive

def _once(a):
    a()
    return 0 #Only one time

n=0

def gRepeatTimer(basetime ,a):
    #gobject.threads_init()
    #gobject.idle_add(a) is the faster timer
    gobject.timeout_add(basetime, _repeat, a )

def gOnceTimer(basetime ,a):
    #gobject.threads_init()
    gobject.timeout_add(basetime,  _once, a )
    

def on_button_clicked(*args):
    #NOTE: RepeatTimer(0.5, greeting)  does not work
    gRepeatTimer(500,greeting)
    gOnceTimer(500,greeting)
    
import inspect
def onDiaLaunched():
    stack=inspect.stack()
    return ("python-startup.py" in stack[-1][1])


if __name__ == '__main__' or not onDiaLaunched():
    
    print("Welcome")
    
    #sleep_timeout(2)  #equivalent to _sleep(2)
    
    #The next 3 bunk of code will not trigger the gui
    #1)
    #tk=Thread(target =  autolaunch_server , args = ())
    #tk.daemon= True
    #tk.start()
    #2)
    #tk=Thread(target = thread , args = (500, autolaunch_server))
    #tk.start()
    #tk.join()
    #3)
    #gobject.timeout_add(500, autolaunch_server )
    
    #the only working way.
    autolaunch_server(None,None)
    
    print("Bye Bye..")
   
    
    
else:
    import dia
    dia.register_action ("Hello", "Hello", 
                     "/DisplayMenu/Debug/DebugExtensionStart", 
                     autolaunch_server )
    

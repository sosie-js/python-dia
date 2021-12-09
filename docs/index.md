# The python Dia Project

Like Chris Daley explained on his article ["An easier way to write Python plugins for Dia"](https://chrisdaley.biz/easy-python-for-dia.html), making python working under Dia is not straightforward because visibility of the documentation and code sample need a deep invetigation to gather the pieces of the puzzle. 

I have thus like many others seeking the python graal to dig into [the grabed dia mailing list by threads](http://sosie.sos-productions.com/python/dia/mail.gnome.org.zip) and extract the python gems provided by Hans Breuer. I used an indexation tool such as DocFetcher to keep the references and be able  to understand how the api works. I discovered by this way Chris dia-mock post on the mailing list and that many samples at that time were only for python2.7 and are not usable unless converting them with 2to3 (if succeed!)

In fact, already in 2006, I built a tool to generate .dia files dynamicaly with js ans PHP but my code refused to work anymore. So this time, I took the opportunity to learn python on this concrete project: A library for producing and manipulating [Dia diagrams](http://dia-installer.de/) files.

## Motivations

I am not the [only one that need to produce diagrams without Gui](https://gitlab.gnome.org/GNOME/dia/-/issues/492), much more faster.

## Demo

![Demo live](https://raw.githubusercontent.com/sosie-js/python-dia/main/pythondia_demo.gif)


1. Simply put the tests/diapyhton.py in your ~/.dia/python and proceed the following installatiob
if you want to run the script in a dual python 2-3 environment when dia is launched. You should see
the debug menu appear with this entry:

![image](https://user-images.githubusercontent.com/70700670/145476191-9c7864ea-13e7-44ea-8244-c1c89df0b915.png)

2. click on it to have your pythondia script executed!

## Installation 

Most of the linux provides dia with python still 2.7 which support ended on janary 2020. 
Moreover python code is not compatible with python3 and having dia with python2 and python3. 
will still be usefull for testing python on both to have universal compatibility
and help you to migrate from each to another.

1) Compile Dia
```sh
cd ~
git clone https://gitlab.gnome.org/GNOME/dia.git
cd dia
meson setup --wipe build --prefix=/opt --buildtype=release 
#Desactivate the buggy pdf, by editing plug-ins/meson.build 
#  and comment the line pdf to have #subdir('pdf')
meson setup  build --reconfigure 
cd build &&meson --prefix=/opt --buildtype=release .. && ninja && ninja install
cd /opt/share/dia
sudo ln -s . data #Ugly hack to make DIA_BASE_PATH happy!
```

2) Import a dia python3 script into user dia python dir. 
```sh
cp /opt/share/dia/python/gtkcons.py ~/.dia/python/gtkcons3.py #Python console serves as test
```

3) Run `dia#2`
```sh
export DIA_LIB_PATH=/opt/lib/x86_64-linux-gnu/dia
export DIA_BASE_PATH=/opt/share/dia
export PYTHONPATH=/usr/local/lib/python3.9/site-packages:/usr/lib/python3/dist-packages
/opt/bin/dia
```

4) Run  `dia#1`
```sh
unset DIA_LIB_PATH
unset DIA_BASE_PATH
unset PYTHONPATH #Will use /usr/bin/python -> /usr/bin/python2 -> /usr/bin/python2.7 MATCHING DIA BUILTIN VERSION
/usr/bin/dia
```
and voilà, that's all folks!

![image](https://gitlab.gnome.org/GNOME/dia/uploads/d20b62cb6f71d5f27fa6f6eb12dd3bd3/image.png)

## Plugins

- [Mock](https://sosie-js.github.io/python-dia/mock) simulates dia core without dia..to avoid
op/close dia each time you change your python code to see the results.

- [Gui](https://sosie-js.github.io/python-dia/gui) the graphical user interface for the Mock plugin
which bring mainly dia.register_action to trigger action from menu mocking the dia interface.



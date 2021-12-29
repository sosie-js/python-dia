# Gui plugin for Python Dia 

Best Gui compagnon for the [dia mocking plugin](https://github.com/sosie-js/python-dia-mock-plugin) (and my first python Gtk app).

## Environnement Dual Python2/3

![image](https://user-images.githubusercontent.com/70700670/144463229-4f2a4c7b-7aff-47e4-8576-53c1ce4451dc.png)

## Limitations

- Only about and quit actions are implemented, we are far form the Dia interface
maybe by combining this with [gaphor](https://github.com/gaphor)..
-the about displays all python, Gtk versions numbers in linux and paths (guess)
- Resizing widow does not resize the view
- nothing can be drawn of the view

## Usage 

1. Follow the tutorial  to install [dia mock](https://sosie-js.github.io/python-dia/mock/)


2. Add your action into the main() body in the 
 and trigger it you will show the gui with the menuitem entry to trigger your action.

```python

#
menu_name="Help" #in which menu you want to be added File, View,...

menuitem_label="About" #the text for your action you will see in the menu
menuitem_tooltip="About Help" #text that give a description/hint when mouse is over (does not show in menu)
menuitem_name="HelpAbout" #registration name, unique generally menu_name+menuitem_label

callback=help_about_callback #handler when action menuitem is clicked

#and the registration
dia.register_action (menuitem_label, menuitem_tooltip, 
                     "/DisplayMenu/"+menu_name+"/"+menuitem_name, 
                     callback)

```

3. Trigger it, use the run_python.sh helpers. Beware of PYTHONPATH , should *match your python version*!


```bash
source run_python2.sh or source run_python3.sh 
```


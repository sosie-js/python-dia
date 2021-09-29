"""
  pydia: objects.py - 2021.09
  ================================================
  
  Note: Experimental, will be obsolete if we found a way to use libdia /pydia libraries
  Author: SoSie@sos-productions.com
  License: LGPL
"""
import _once

# Core (DON'T TOUCH THESE TWO LINES!)
from .objects.UML.Class import DIA_UML_Class
from .ObjectHelpers import DiaObjectFactoryHelper

# Extras
from .objects.database.table import DIA_database_Table

# Should be the last
from .ObjectHelpers import DIA_CSV_parser


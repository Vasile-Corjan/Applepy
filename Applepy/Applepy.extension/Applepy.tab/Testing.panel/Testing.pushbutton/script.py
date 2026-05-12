# -*- coding: utf-8 -*-
# Created by Vasile Corjan
import clr
clr.AddReference("RevitServices")
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
from Autodesk.Revit.Exceptions import InvalidOperationException
import System, os
from System import Enum

# pyRevit
import pyrevit
from pyrevit import revit,DB,HOST_APP
from pyrevit import forms,script
from pyrevit.coreutils import Timer

doc = revit.doc
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
active_view = doc.ActiveView

output = script.get_output()
output.close_others()
timer = Timer()

# Collect RevitLinkInstances
links = DB.FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# Get the Document of the LinkedInstance
linked_doc = links[0].GetLinkDocument()

# Acquiring the Coordinates
with revit.Transaction("Acquire Coordinates"):
	try:
		doc.AcquireCoordinates(links[0].Id)
		output.print_md("### <font color='green'>The coordinates are acquired</font>")
	except InvalidOperationException as ex:
		output.print_md("### <font color='red'>Error: {}</font>".format(ex.Message))
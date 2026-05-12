# -*- coding: utf-8 -*-
# Created by Vasile Corjan
import clr
clr.AddReference("RevitServices")
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
import System
from System import Enum

# pyRevit
from pyrevit import forms, script, revit, DB, HOST_APP
from pyrevit.coreutils import Timer

# Initialize Revit API objects
doc = revit.doc
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
active_view = doc.ActiveView

output = script.get_output()
output.close_others()
timer = Timer()

# COLLECT THE NECESSARY ELEMENTS  
# All Revit Link instances in the current document
links = DB.FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

if not links:
	forms.alert("No Revit links found in the current document.", exitscript=True)

# Select the desired Revit link from the list
revit_instance_names = {link.Name:link for link in links}
selected_linked_model = forms.SelectFromList.show(sorted(revit_instance_names), title="Select the linked model", button_name="Select")
linked_model = revit_instance_names.get(selected_linked_model)

# Getting the Revit Link Document
linked_doc = linked_model.GetLinkDocument()

# Levels and grids
levels_in_linkdoc = DB.FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElementIds()
grids_in_linkdoc =  DB.FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()

if not levels_in_linkdoc and not grids_in_linkdoc:
	forms.alert("No Levels or Grids found in the current document.", exitscript=True)

# Combining Grids and Levels lists into one
elements_to_copy = List[ElementId]()
elements_to_copy.AddRange(levels_in_linkdoc)
elements_to_copy.AddRange(grids_in_linkdoc)

# PREPERING THE VARIABLES FOR COPYING
transform = Transform.Identity
opts = CopyPasteOptions()

# Copying the elements
with revit.Transaction("Copy selected linked elements"):
	ElementTransformUtils.CopyElements(linked_doc, elements_to_copy, doc, transform, opts)

forms.alert("Successfully copied {} elements (Levels and Grids) from the linked document.".format(elements_to_copy.Count), title="Success")
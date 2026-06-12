# -*- coding: utf-8 -*-
# Created by Vasile Corjan

import clr
clr.AddReference("RevitServices")
from Autodesk.Revit.DB import *
from Autodesk.Revit.Exceptions import ArgumentException

import System
from System.Collections.Generic import List

# pyRevit
from pyrevit import forms, script, revit, DB


# Initialize Revit API objects
doc = revit.doc
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
active_view = doc.ActiveView

# --- MAIN SCRIPT ---

# ALL REVIT LINK INSTANCES IN THE CURRENT DOCUMENT
links = DB.FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

if not links:
	forms.alert("No Revit links found in the current document.", exitscript=True)

# SELECT THE DESIRED REVIT LINK FROM THE LIST
revit_instance_names = {link.Name:link for link in links}
selected_linked_model = forms.SelectFromList.show(
	sorted(revit_instance_names),
	title="Select the linked model",
	button_name="Select")
if not select_linked_model:
	script.exit()

linked_model = revit_instance_names.get(selected_linked_model)

# GETTING THE REVIT LINK DOCUMENT
linked_doc = linked_model.GetLinkDocument()

# PICK LINKED ELEMENTS
elements_to_copy = revit.pick_linkeds()
if not elements_to_copy:
	forms.alert("No elements were selected. Exiting.", exitscript=True)
elements_category = {e.Category.Name for e in elements_to_copy}

# GET ELEMENT IDS
element_ids = List[ElementId]()
for element in elements_to_copy:
	element_ids.Add(element.Id)

# PREPERING THE VARIABLES FOR COPYING
transform = Transform.Identity
opts = CopyPasteOptions()

# COPYING THE ELEMENTS
with revit.Transaction("Copy selected linked elements"):
	try:
		ElementTransformUtils.CopyElements(linked_doc, element_ids, doc, transform, opts)
	except ArgumentException as e:
		forms.alert("You are trying to copy view specific elements such as lines, filled regions, detail items etc.", exitscript=True)

forms.alert("Successfully copied {} elements {} from the linked document.".format(elements_to_copy.Count, elements_category), title="Success")
# -*- coding: utf-8 -*-
# Created by Vasile Corjan
import clr
clr.AddReference("RevitServices")
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
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

links = DB.FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
revit_instance_names = {link.Name:link for link in links}
selected_linked_model = forms.SelectFromList.show(sorted(revit_instance_names), title="Select the linked model")
linked_model = revit_instance_names.get(selected_linked_model)

linked_doc = linked_model.GetLinkDocument()

linked_views = DB.FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements() #OST_ElectricalFixtures
revit_instance_views = {link.Name:link for link in linked_views}
selected_linked_view = forms.SelectFromList.show(sorted(revit_instance_views), title="Select the linked view")
linked_view = revit_instance_views.get(selected_linked_view)



#Getting the elements from a linked Document in the host view
elements = DB.FilteredElementCollector(doc,active_view.Id,linked_model.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation).WhereElementIsNotElementType().ToElementIds() #OST_ElectricalFixtures

#Prep variables

transform = Transform.Identity
opts = CopyPasteOptions()

with revit.Transaction("Copy generic annotations from views"):
	ElementTransformUtils.CopyElements(linked_view, elements, active_view, transform, opts)

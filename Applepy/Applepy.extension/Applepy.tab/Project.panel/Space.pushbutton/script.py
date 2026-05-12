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

output = script.get_output()
output.close_others()
timer = Timer()

version = HOST_APP.version
#print(version, type(version))

properties = DB.ParameterUtils.GetAllBuiltInGroups()
active_level = doc.ActiveView.GenLevel

links = DB.FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
revit_instance_names = {link.Name:link for link in links}
selected_linked_model = forms.SelectFromList.show(sorted(revit_instance_names), title="Select the linked model")
linked_model = revit_instance_names.get(selected_linked_model)
transform = linked_model.GetTotalTransform()
host_levels = {lvl.Name: lvl for lvl in DB.FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()}

linked_doc = linked_model.GetLinkDocument()

linked_rooms = DB.FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

new_spaces = []
with revit.Transaction("Create Space"):
	for room in linked_rooms:
		if not room.Location:
			continue
		
		room_level_name = room.Level.Name
		room_point = room.Location.Point
		create_point = DB.UV(room_point.X, room_point.Y)
		host_level = host_levels.get(room_level_name)
		#host_point = transform.OfPoint(room_point)
		
		new_space = doc.Create.NewSpace(host_level, create_point)
		new_spaces.append(new_space)

output.print_md("Rooms in the linked model: {}".format(len(linked_rooms)))
output.print_md("Spaces created: {}".format(len(new_spaces)))


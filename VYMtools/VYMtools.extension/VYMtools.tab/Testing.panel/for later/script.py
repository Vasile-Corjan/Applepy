# -*- coding: utf-8 -*-
# Created by Vasile Corjan
# Regular + Autodesk
import clr
clr.AddReference("RevitServices")
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
import os, System

# pyRevit
import pyrevit
from pyrevit import revit,DB
from pyrevit import forms,script
from pyrevit.coreutils import Timer

doc = revit.doc
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

logger = script.get_logger()
output = script.get_output()
output.close_others()
timer = Timer()

# Get all the categories
selection = revit.pick_elements()
for el in selection:
	reference = Reference(el)
	print(reference)
categories = list(System.Enum.GetValues(BuiltInCategory))
selected_tag_category = forms.SelectFromList.show(categories, title="Select the category of the tag")

collector = FilteredElementCollector(doc).OfCategory(selected_tag_category)
tags = collector.ToElements()

tag_list = []

for t in tags:
	if t.GetType().Name == "FamilySymbol": 
		value = ("{} : {}").format(t.FamilyName, Element.Name.GetValue(t))
		tag_list.append(t)
	

selected_tag = forms.SelectFromList.show(tag_list, title="Select the tag")

selected_views = forms.select_views()


#TagModel.TM_ADDBY_CATEGORY

with revit.Transaction('Tag All Selected Elements'):
	for view in selected_views:
		for el in selection:
			#reference = Reference(el)
			leader = False
			element_center = el.Location.ToPoint()
			try:
				#element_tag = IndependentTag.Create(doc, selected_tag.Id, view.Id, Reference(el), leader, TagOrientation.Horizontal, element_center)
				element_tag = IndependentTag.Create(doc, view.Id, Reference(el), leader,TagMode.TM_ADDBY_CATEGORY, TagOrientation.Horizontal, element_center)
			except TypeError as e:
				print("Caught a TypeError:", e)
				
			# # if isinstance(view, DB.ViewSection):
				# # element_tag.Location.Move(DB.XYZ(0, 0, element_center.Z))

""" 
✅ collect all the tags in the document by the category.
Create a tag
IndependentTag.Create(doc,elementId(tagelement),elementId(View),reference(elementreference),addLeader(bool),
TagOrientation,XYZ(point))
"""
# # UI selection of the elements 
# list_untagged_fixture_ids = List[ElementId](untagged_fixtures_id)
# uidoc.Selection.SetElementIds(list_untagged_fixture_ids)
# if not element_center:
				# logger.debug('Can not detect center for element: {}',output.linkify(el.Id))
				# continue
			# if isinstance(view, (DB.ViewSection, DB.ViewPlan)):
				# logger.debug('Working on view: %s',revit.query.get_name(view))
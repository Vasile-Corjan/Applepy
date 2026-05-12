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

output = script.get_output()
output.close_others()
timer = Timer()


# Get all the all_categories
all_categories = list(System.Enum.GetValues(BuiltInCategory))

# Select the all_categories
selected_element_category = forms.SelectFromList.show(all_categories, title="Select the category of the element")

	
selected_tag_category = forms.SelectFromList.show(all_categories, title="Select the category of the tag")

if selected_element_category or selected_tag_category:
	script.exit()

tag_elements_collector = FilteredElementCollector(doc).OfCategory(selected_tag_category).WhereElementIsElementType()
available_tag_families = {tag.FamilyName for tag in tag_elements_collector}
selected_tag_family = forms.SelectFromList.show(available_tag_families, title="Select the tag type")

selected_views = forms.select_views()

def filter_elements_by_fam_name(selected_tag_family):
    family_name_param_id = ElementId(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
    family_parameter = ParameterValueProvider(family_name_param_id)
    evaluator = FilterStringEquals()
    f_rule = FilterStringRule(family_parameter, evaluator, selected_tag_family) 
    filter_fam_name = ElementParameterFilter(f_rule)
    filtered_tag_elements = FilteredElementCollector(doc).WherePasses(filter_fam_name).WhereElementIsNotElementType().ToElements()

    return filtered_tag_elements

filtered_tag_elements = filter_elements_by_fam_name(selected_tag_family)

#Collect all elements in the view
def find_untagged_elements(view, element_cat, tags):
    collector_1 = FilteredElementCollector(doc, view.Id).OfCategory(element_cat)
    #collector_2 = FilteredElementCollector(doc, view.Id).OfCategory(tag_cat)
    all_fixtures = collector_1.WhereElementIsNotElementType().ToElements()
    #tags = collector_2.WhereElementIsElementType().ToElements()
    
    tagged_elements = []
    
    for tag in tags:
        tag_element = tag.GetTaggedLocalElements()
        tagged_elements.extend(tag_element)
        
    tagged_element_ids = [e.Id for e in tagged_elements]
    untagged_element_ids = [e.Id for e in all_fixtures if e.Id not in tagged_element_ids]
    
    return untagged_element_ids


# Output the results
output.print_md("# Missing tags")
output.print_md("---")

for view in selected_views:
    untagged_elements_ids = find_untagged_elements(view, selected_element_category, filtered_tag_elements)
    linkify_view = output.linkify(view.Id, view.Name)
    output.print_md("### View: {}".format(linkify_view))
    
    if untagged_elements_ids:
        for element_id in untagged_elements_ids:
            element = doc.GetElement(element_id)
            linkify_element = output.linkify(element_id, element.Name)
            print("Missing a tag: {}".format(linkify_element))
    else:
        output.print_md("### All elements in *{}* are tagged :thumbs_up:".format(view.Name))
    
    output.print_md("---")

output.print_md("Script execution time :timer_clock: : {:.4f} seconds".format(timer.get_time()))

# # UI selection of the elements 
# list_untagged_fixture_ids = List[ElementId](untagged_fixtures_id)
# uidoc.Selection.SetElementIds(list_untagged_fixture_ids)
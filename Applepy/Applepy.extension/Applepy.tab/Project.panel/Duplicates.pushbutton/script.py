# -*- coding: utf-8 -*-
# Created by Vasile Corjan
# Regular + Autodesk
from Autodesk.Revit.DB import *
import System
import os

# pyRevit
import pyrevit
from pyrevit import revit,DB
from pyrevit import forms,script
from System.Collections.Generic import List
from pyrevit.coreutils import Timer
from collections import defaultdict

doc = revit.doc
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

output = script.get_output()
output.close_others()
timer = Timer()
WARNING_GUID = ["b4176cef-6086-45a8-a066-c3fd424c9412"]


# 1. Get Elements
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ElectricalFixtures)
all_elements = collector.WhereElementIsNotElementType().ToElements()

warnings = doc.GetWarnings()
warn_elements = []
for w in warnings:
    if w.GetFailureDefinitionId().Guid.ToString() in WARNING_GUID:
            warn_elements.append(w.GetFailingElements())
           
for e in warn_elements:
    print("Elements {} have the same placement".format(output.linkify(e)))

print("Script execution time: {:.4f} seconds".format(timer.get_time()))
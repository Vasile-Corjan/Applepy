# pyRevit
import pyrevit
from pyrevit import revit,DB
from pyrevit import forms,script

from Autodesk.Revit.DB import *
import System
import os
import time


doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
active_view_id = view.Id
folder = r'C:\Users\Bruger\Desktop'


# Set IFC export options
options = IFCExportOptions()

options.FileVersion = IFCVersion.IFC4
options.AddOption("ExportBaseQuantities", "True")
options.FilterViewId = active_view_id

ifc_options = DB.IFCExportOptions(options)


# Export the view to IFC
with revit.Transaction('IFC export'):
	doc.Export(folder, doc.Title + ".ifc", ifc_options)



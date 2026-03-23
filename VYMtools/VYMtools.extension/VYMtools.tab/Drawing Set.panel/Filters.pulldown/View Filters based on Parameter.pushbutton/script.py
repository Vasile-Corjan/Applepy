import pyrevit
from pyrevit import revit,DB
from pyrevit import forms,script
from System.Collections.Generic import List


doc = revit.doc
uidoc = revit.ActiveUIDocument

# Get all view filters
all_par_filters = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
all_par_filter_names = [f.Name for f in all_par_filters]


# Start Transaction
with revit.Transaction('Create view filters'):
    
    for element_type_name in element_type_names:
        filter_name = 'Type_{}'.format(element_type_name)
        if not filter_name in all_par_filter_names:
            
    
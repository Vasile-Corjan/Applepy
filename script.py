import pyrevit
from pyrevit import revit,DB
from pyrevit import forms,script
from System.Collections.Generic import List


doc = revit.doc
doc_from = forms.select_open_docs(title='Select the source document',
                                    button_name='Select',
                                    width= 500,
                                    multiple=False)

if not doc_from:
    forms.alert("No Revit document selected", exitscript=True)
elif doc_from.IsFamilyDocument:
    forms.alert("Must choose a non-family document", exitscript=True)
    
# Get all views from the document
all_views = DB.FilteredElementCollector(doc_from).OfCategory(DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

# Get all views with filter	
views_with_filter = [v for v in all_views if v.GetFilters()]
dict_views_with_filters = {i.Name:i for i in views_with_filter}

selected_src_view = forms.SelectFromList.show(sorted(dict_views_with_filters),
                                            title='Select the source View/ViewTemplate',
                                            multiselect=False,
                                            button_name='Select source View/ViewTemplate',
                                            filterfunc = lambda x: isinstance(x,DB.ViewPlan),
                                            use_selection=True)
if not selected_src_view:
	script.exit()
	
# Select the filters from the source view
src_view = dict_views_with_filters[selected_src_view]
filters = sorted([doc_from.GetElement(f_id) for f_id in src_view.GetFilters()])

selected_filters = forms.SelectFromList.show(filters,
                                            title='Select source filters',
                                            multiselect=True,
                                            button_name='Select source filters',
											name_attr = "Name")
if not selected_filters:
	script.exit()

# Select the destination views
dest_views = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
dict_dest_views = {v.Name:v for v in dest_views}

selected_dest_view = forms.SelectFromList.show(sorted(dict_dest_views),
                                            title='Select the destination View/ViewTemplate',
                                            multiselect=True,
                                            button_name='Select destination View/ViewTemplate')

selected_dest_views = [dict_dest_views[v] for v in selected_dest_view]

if not selected_dest_view:
	script.exit()
	
# Copy the filters to another project

transform = DB.Transform.Identity
opts = DB.CopyPasteOptions()

ids = [e.Id for e in selected_filters]
ids_copy = List[DB.ElementId](ids)

with revit.Transaction('Copy filters'):
	copied = DB.ElementTransformUtils.CopyElements(doc_from,ids_copy,doc,transform,opts)

	for i,view_filter in enumerate(selected_filters):
		filter_overrides = src_view.GetFilterOverrides(view_filter.Id)
		for view in selected_dest_views:
			view.SetFilterOverrides(copied[i], filter_overrides)
from pyrevit import revit,DB
from pyrevit import forms,script

#get revit document

doc = revit.doc

#get all CAD instances

cad_all = DB.FilteredElementCollector(doc).OfClass(DB.ImportInstance).ToElements()

# get names of all CAD types

type_names = []

for c in cad_all:
    c_type = doc.GetElement(c.GetTypeId())
    t_name = DB.Element.Name.__get__(c_type)
    type_names.append(t_name)

set_names = list(set(type_names))

# group CAD instances by their type names

cad_ids,cad_types,cad_views = [],[],[]

for sn in set_names:
    cad_ids_sub,cad_types_sub,cad_views_sub = [],[],[]
    for cad,na in zip(cad_all,type_names):
        if na == sn:
            cad_ids_sub.append(cad.Id)
            if  cad.IsLinked:
                cad_types_sub.append("Linked instance: ")
            else:
                cad_types_sub.append("Imported instance: ")
            if cad.ViewSpecific:
                cad_views_sub.append(cad.OwnerViewId)
            else:
                cad_views_sub.append("")
    cad_ids.append(cad_ids_sub)
    cad_types.append(cad_types_sub)
    cad_views.append(cad_views_sub)

# get the script output

output = script.get_output()

#report a header
output.print_md("List of all CAD objects:")
print("Click on Id to select or view an object")

#report the CAD instances
for sn,ids,links,views in zip(set_names,cad_ids,cad_types,cad_views):
    print('\n' + sn + ":")
    for i,l,v in zip(ids,links,views):
        if v == "":
            print(l + 'id {}'.format(output.linkify(i)) + " is not view specific.")
        else:
            print(l + 'id {}'.format(output.linkify(i)) + " specific to the view " + 'id {}'.format(output.linkify(views)))
    print('\n')
    
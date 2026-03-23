# Created by Vasile Corjan
import pyrevit
from pyrevit import revit,DB
from pyrevit import script,forms

# Files location
directory = "C:\Dropbox\Dropbox (DanskEl&EnergiApS)\Dansk El & Energi ApS\Arbejdsdokumenter\Revit\DEE_REVIT"
#directory = os.path.expanduser('~')

# get Revit Document
doc = revit.doc

# Selecting the families to load into the project
family_path = forms.pick_file(file_ext='rfa',multi_file=True,init_dir=directory,
	title='Select the families')

if not family_path:
	script.exit()
	
# Loading the selected families
trans = DB.Transaction(doc,'Load Family')

trans.Start()
for family in family_path:
	doc.LoadFamily(family)
trans.Commit()
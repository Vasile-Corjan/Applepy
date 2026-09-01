# -*- coding: utf-8 -*-
# Created by Vasile Corjan

import re
import os
from System import Enum

from Autodesk.Revit.DB import *
from System.Collections.Generic import List

# pyRevit
import pyrevit
from pyrevit import revit,DB,HOST_APP
from pyrevit import forms,script

doc = revit.doc
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
active_view = doc.ActiveView

console = script.get_output()
console.set_height(800)
logger = script.get_logger()


def parse_html(file_path):
	with open(file_path, 'r') as f:
		html = f.read()

	data = []

	# Find all table rows
	rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.I | re.S)

	for row in rows:
		# Find all cells in the row
		cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.I | re.S)

		# Remove any nested HTML tags and whitespace
		cleaned = []
		for cell in cells:
			text = re.sub(r'<[^>]+>', '', cell)
			cleaned.append(text.strip())

		if len(cleaned) >= 3:
			data.append({
				"ID": cleaned[0],
				"Element_1": cleaned[1],
				"Element_2": cleaned[2]
			})
	return data

#Convert the id into ElementID (clickable)
def element_id(text):
		match = re.search(r"id (\d+)", text)
		if not match:
			return text
		if match and match.group(1).isdigit():
			link = console.linkify(DB.ElementId(int(match.group(1))))
			return text.replace(match.group(1), link)

html_file = forms.ask_for_string(prompt= 'Insert the path to the exported html element', title='Path').strip('"')

if (os.path.isfile(html_file)):
	interference_data = parse_html(html_file)
	interference_data.pop(0)
	interference_data = [[d["ID"], d["Element_1"], d["Element_2"]] for d in interference_data]

	table_data = [map(element_id, item) for item in interference_data]

	console.print_md('##CLASH TABLE')
	console.insert_divider()
	console.print_md('###Total clashes found: **{}**'.format(len(interference_data)))
	console.print_html_table(table_data=table_data,
		columns=["ID","Element_1","Element_2"],
		column_head_align_styles=["center", "center", "center"],
		column_data_align_styles=["center", "left", "left"],
		row_striping = True,)
	console.save_contents(r'C:\Users\Bruger\Desktop\result.html')
	
	
print (logger)
# -*- coding: utf-8 -*-
# Created by Vasile Corjan
import xlrd
from pyrevit import forms

file = forms.pick_file(file_ext='*',init_dir = r'C:\Users\Bruger\Desktop',
    title = 'Select the Excel file')

def _read_xlsheet(xlsheet, columns=[], datatype=None, headers=False):
    xlsheetdata = []
    xlsheetrows = list(xlsheet.get_rows())
    skip = 1 if headers else 0
    xlsheetheader = [x.value for x in xlsheetrows[0]] if headers else []
    for xlsheetrow in xlsheetrows[skip:]:
        drow = list([x.value for x in xlsheetrow])
        if columns:
            drow = dict([x for x in zip(columns, drow)])
        elif datatype:
            drow = datatype(drow)
        xlsheetdata.append(drow)
    return {'headers': xlsheetheader, 'rows': xlsheetdata}
    

def load(xlfile, sheets=[], columns=[], datatype=None, headers=True):
    xldata = {}
    xlwb = xlrd.open_workbook(xlfile)
    for xlsheet in xlwb.sheets():
        if sheets:
            if xlsheet.name in sheets:
                xldata[xlsheet.name] = _read_xlsheet(xlsheet,
                                                     columns=columns,
                                                     datatype=datatype,
                                                     headers=headers)
        else:
            xldata[xlsheet.name] = _read_xlsheet(xlsheet,
                                                 columns=columns,
                                                 datatype=datatype,
                                                 headers=headers)
    return xldata

print(load(file))
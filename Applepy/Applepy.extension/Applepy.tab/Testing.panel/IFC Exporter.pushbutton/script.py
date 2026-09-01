#! python3
# pyRevit
import pyrevit
from pyrevit import revit,DB
from pyrevit import forms,script

from Autodesk.Revit.DB import *
import System
import os
import time
import inspect


out = script.get_output()

print(out._runtime_output())
print(type(out._runtime_output()))

for name in dir(out):
    if "table" in name.lower():
        print(name)

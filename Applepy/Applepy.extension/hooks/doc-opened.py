# -*- coding: utf-8 -*-
from pyrevit.script import store_data
from pyrevit.coreutils import current_time

# Getting the opening time
start_time = current_time()
store_data("Project opened", start_time, this_project=True)
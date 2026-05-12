# -*- coding: utf-8 -*-
# Created by Vasile Corjan
import os
import shutil
from pyrevit import script
from pyrevit.coreutils import Timer
import wpf
from System.Windows import Window
from System.Windows.Forms import FolderBrowserDialog, DialogResult

class FileRenamer(Window):
    def __init__(self, xaml_path):
        wpf.LoadComponent(self, xaml_path)
        self.ShowDialog()
    
    def cancel_window(self, sender, event):
        self.Close()
        
    def search_directory(self, sender, event):
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.FindName("LocationTextBox").Text = dialog.SelectedPath

    def get_textbox_value(self, textbox_name):    
        return self.FindName(textbox_name).Text.strip()

    def rename_files(self, sender, event):
		timer = Timer()
		prefix = self.FindName("PrefixTextBox").Text
		replace = self.get_textbox_value("ReplaceTextBox")
		directory = self.get_textbox_value("LocationTextBox")

		if not directory:
			print("No directory was chosen.")
			return

		if not os.path.isdir(directory):
			print("Invalid directory path.")
			return

		os.chdir(directory)
		files_renamed = 0

		for file in os.listdir(directory):
			name, ext = os.path.splitext(file)
			if prefix in name:
				new_name = name.replace(prefix, replace) + ext
				old_path, new_path = os.path.join(directory, file), os.path.join(directory, new_name)
				shutil.move(old_path, new_path)
				files_renamed += 1

		print("File renaming completed successfully: {} files renamed".format(files_renamed))
		print("Script execution time: {:.4f} seconds".format(timer.get_time()))
		self.Close()

if __name__ == "__main__":
    
    
    script_path = os.path.dirname(__file__)
    xaml_file_path = os.path.join(script_path, 'multi-input-ui.xaml')
	
    FileRenamer(xaml_file_path)

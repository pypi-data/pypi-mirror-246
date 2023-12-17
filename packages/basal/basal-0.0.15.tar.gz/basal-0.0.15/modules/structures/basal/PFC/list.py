


'''
	import basal.PFC.list as PFC_list
	PFC_list = PFC_list.start ()
'''

import basal.climate as basal_climate
from pathlib import Path

import os

def start ():	
	PFC = basal_climate.find ("PFC")	
	PFC_path = PFC ['path']
	
	directory_names = []
	for trail in Path (PFC_path).iterdir ():
		name = os.path.relpath (trail, PFC_path)
		
		if trail.is_dir ():
			directory_names.append (name)
	
		else:
			raise Exception (f'found a path that is not a directory: \n\n\t{ name }\n')
		
	
		'''
		if trail.is_file ():
			print(f"{trail.name}:\n{trail.read_text()}\n")
		'''
		
	return directory_names;
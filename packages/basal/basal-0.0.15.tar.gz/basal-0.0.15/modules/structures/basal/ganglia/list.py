


'''
	import basal.ganglia.list as basal_ganglia_list
	basal_ganglia_list.start ()
'''

import basal.climate as basal_climate
from pathlib import Path

import os

def start ():	
	basal_ganglia = basal_climate.find ("basal ganglia")	
	basal_ganglia_path = basal_ganglia ['path']
	
	directory_names = []
	for address in Path (basal_ganglia_path).iterdir ():
		address_name = os.path.relpath (address, basal_ganglia_path)
		
		if address.is_dir ():
			for basal_module in Path (address).iterdir ():
				basal_module_name = os.path.relpath (basal_module, address)
			
				directory_names.append ([
					address_name,
					basal_module_name
				])
				
	
		else:
			raise Exception (f'found a path that is not a directory: \n\n\t{ name }\n')
		
	
		'''
		if trail.is_file ():
			print(f"{trail.name}:\n{trail.read_text()}\n")
		'''
		
	return directory_names;

import pandas as pd
from copy import deepcopy
from nettoolkit.nettoolkit_db import *
from nettoolkit.nettoolkit_common import *
from .devices import AdevDevices, device_df_drop_empty_duplicates, update_var_df_details_to_table_df
from .cablings import ADevCablings
from .maths import CalculateXY
from .general import *

pd.set_option('mode.chained_assignment', None)


# --------------------------------------------- 
# Data Frame Generator
# --------------------------------------------- 
class DFGen():
	"""DataFrame generator

	Args:
		files (list): list of input excel -clean files 
	"""	
	def __init__(self, files):
		"""initializer of DF Generator
		"""		
		self.files = files
		self.default_stencil = None
		self.default_x_spacing = 3.5
		self.default_y_spacing = 2
		self.line_pattern_style_separation_on = None
		self.line_pattern_style_shift_no = 2
		self.func_dict = {}
		self.var_func_dict = {}
		self.pattern = 1
		self.blank_dfs()

	def blank_dfs(self):
		"""creates devices/cabling blank DataFrames
		"""		
		self.devices_merged_df = pd.DataFrame({'hostname':[]})
		self.cabling_merged_df = pd.DataFrame({'a_device':[]})

	def custom_attributes(self, **kwargs):
		"""add/update custom attributes for object
		"""		
		for k, v in kwargs.items():
			if v:
				self.__dict__[k] = v

	def custom_functions(self, **kwargs):
		"""add/update custom functions for object
		"""		
		for k, v in kwargs.items():
			self.func_dict[k] = v

	def custom_var_functions(self, **kwargs):
		"""add/update custom `var` tab functions for object
		"""		
		for k, v in kwargs.items():
			self.var_func_dict[k] = v

	def run(self):
		"""iterate over all files for generating devices/cabling DataFrame details.
		"""		
		self.DCT = {}
		for file in self.files:
			DCT = DF_ConverT(file, self.default_stencil, self.line_pattern_style_separation_on, self.line_pattern_style_shift_no)
			DCT.get_self_details(self.var_func_dict)
			DCT.convert(self.func_dict)
			self.update_devices_df(DCT, file)
			self.update_cabling_df(DCT, file)
			self.DCT[DCT.hostname] = DCT

		self.devices_merged_df = device_df_drop_empty_duplicates(self.devices_merged_df)
		self.devices_merged_df = update_var_df_details_to_table_df(self.devices_merged_df, self.DCT, self.var_func_dict)
		#
		# self.calculate_cordinates()  # do after update for multi tab calculations (delete line in next release)
		#
		self.cabling_merged_df.reset_index(inplace=True)
		self.remove_duplicate_cabling_entries()
		self.remove_undefined_cabling_entries()
		#
		self.df_dict = {'Devices': self.devices_merged_df, 'Cablings': self.cabling_merged_df }
		#

	def update(self, *funcs):
		for f in funcs:
			f(self.df_dict)

	def update_devices_df(self, DCT, file):
		"""update Devices DataFrame

		Args:
			DCT (DF_ConverT): DataFrame Convertor object
			file (str): a single database. -clean excel file. ( not in use )
		"""		
		ddf = DCT.update_devices()
		#
		# ddf_dev = DCT.update_device_self_detils(self.func_dict)
		# ddf = pd.concat([ddf, ddf_dev], axis=0, join='outer')
		#
		self.devices_merged_df = pd.concat([self.devices_merged_df, ddf], axis=0, join='outer')

	def update_cabling_df(self, DCT, file):
		"""update Cabling DataFrame

		Args:
			DCT (DF_ConverT): DataFrame Convertor object
			file (str): a single database. -clean excel file.
		"""		
		cdf = DCT.update_cablings(**self.__dict__)
		#
		self.cabling_merged_df = pd.concat([self.cabling_merged_df, cdf], axis=0, join='outer')

	def calculate_cordinates(self, sheet_filter_dict={}):
		"""calculate the x,y coordinate values for each devices and keep Devices, Cablings DataFrame Dictionary ready.

		Args:
			sheet_filter_dict (dict): sheet filter dictionary for mutitab executions.
		"""		
		if self.cabling_merged_df.empty: return
		CXY = CalculateXY(self.devices_merged_df, self.default_x_spacing, self.default_y_spacing, self.cabling_merged_df, sheet_filter_dict)
		CXY.calc()
		self.df_dict = {'Devices': CXY.df, 'Cablings': self.cabling_merged_df }

	def remove_duplicate_cabling_entries(self):
		"""removes duplicate cabling entries between a-b devices
		"""		
		a_to_b = {}
		copy_full_df = deepcopy(self.cabling_merged_df)
		for i, data in copy_full_df.iterrows():
			if not a_to_b.get(data.a_device):
				a_to_b[data.a_device] = {'remotedev':[]}
			if data.b_device in a_to_b.keys() and data.a_device in a_to_b[data.b_device]['remotedev']:
				self.cabling_merged_df.drop(i, inplace=True)
				continue
			if data.a_device in a_to_b.keys() and data.b_device in a_to_b[data.a_device]['remotedev']:
				self.cabling_merged_df.drop(i, inplace=True)
				continue
			a_to_b[data.a_device]['remotedev'].append(data.b_device)

	def remove_undefined_cabling_entries(self):
		"""removes undefined cabling entries where device doesn't exist in devices tab
		"""		
		dev_hosts = set(self.devices_merged_df.hostname) 
		copy_full_df = deepcopy(self.cabling_merged_df)
		for i, data in copy_full_df.iterrows():
			if not data.a_device in dev_hosts or not data.b_device in dev_hosts:
				self.cabling_merged_df.drop(i, inplace=True)
				continue


# --------------------------------------------- 
# Data Frame Converter
# --------------------------------------------- 
class DF_ConverT():
	"""Data Frame Converter

	Args:
		file (str): a single database. -clean excel file.
		default_stencil (str): default visio stencil file.
		line_pattern_style_separation_on (str): column name on which line pattern separation should be decided on
		line_pattern_style_shift_no (int): line pattern change/shift number/steps
	"""	

	def __init__(self, file, 
		default_stencil, 
		line_pattern_style_separation_on, 
		line_pattern_style_shift_no,
		):
		"""object initializer
		"""		
		self.file = file
		self.full_df = read_xl(file)
		file = file.split("/")[-1].split("\\")[-1]
		self.self_device = file.split("-clean")[0].split(".")[0]
		#
		self.stencils = default_stencil
		self.line_pattern_style_separation_on = line_pattern_style_separation_on
		self.line_pattern_style_shift_no = line_pattern_style_shift_no


	def get_self_details(self, var_func_dict):
		"""update the value from var tab of var function dictionary

		Args:
			var_func_dict (dict): custom var functions dictionary
		"""		
		self.var_func_dict = var_func_dict
		for k,  f in var_func_dict.items():
			v = f(self.full_df['var'])
			if not v: v = 'N/A'
			self.__dict__[k] = v

	def convert(self, func_dict):
		"""create physical DataFrame, update with patterns  

		Args:
			func_dict (dict): custom functions dictionary
		"""		
		# vlan
		vlan_df = get_vlan_if_up(self.full_df['vlan'])
		vlan_df = get_vlan_if_relevants(vlan_df)
		self.vlan_df = vlan_df

		# physical
		df = get_physical_if_up(self.full_df['physical'])
		df = get_physical_if_relevants(df)
		#
		df = self.update_devices_df_pattern_n_custom_func(df, func_dict)
		#
		self.u_ph_df = df


	def update_devices_df_pattern_n_custom_func(self, df, func_dict):
		"""updates Devices DataFrame patterns as per custom functions provided in func_dict

		Args:
			df (DataFrame): pandas DataFrame for devices
			func_dict (dict): custom functions dictionary

		Returns:
			DataFrame: updated DataFrame
		"""		
		for k, f in func_dict.items():
			df[k] = f(df)
		#
		self.patterns = get_patterns(df, self.line_pattern_style_separation_on, self.line_pattern_style_shift_no)
		df = update_pattern(df, self.patterns, self.line_pattern_style_separation_on)
		#
		return df


	def update_cablings(self, **default_dic):
		"""creates Cabling object and its DataFrame, adds cabling details

		Returns:
			DataFrame: pandas DataFrame
		"""		
		self.C = ADevCablings(self.self_device, **default_dic)
		for k, v in self.u_ph_df.iterrows():
			kwargs = {}
			for x, y in v.items():
				kwargs[x] = y
			self.C.add_to_cablings(**kwargs)
		df = self.C.cabling_dataframe()
		return df

	def update_devices(self):
		"""creates Devices object, and its DataFrame, adds vlan informations.

		Returns:
			DataFrame: updated pandas DataFrame for interface connected devices
		"""		
		self.D = AdevDevices(self.stencils, self.var_func_dict, self.full_df['var'])
		self.D.int_df = self.update_devices_for(df=self.u_ph_df, dic=self.D.devices)
		self.D.add_vlan_info(self.vlan_df)
		return self.D.merged_df

	def update_device_self_detils(self, func_dict):
		"""create a pandas DataFrame object for the self object using `var` tab and custom functions

		Args:
			func_dict (dict): custom var functions

		Returns:
			DataFrame: pandas DataFrame for self device
		"""		
		self_device_df = self.D.get_self_device_df()
		self_dev_df = self.update_devices_for(df=self_device_df, dic=self.D.self_device)
		self_dev_df = self.update_devices_df_pattern_n_custom_func(self_dev_df, func_dict, True)
		return self_dev_df

	def update_devices_for(self, df, dic):
		"""update DataFrame for the provided dictionary (dic) objects, and removes empty and duplicate hostname value rows.

		Args:
			df (DataFrame): variable DataFrame
			dic (dict): variable dictionary

		Returns:
			DataFame: updated DataFrame
		"""		
		for k, v in df.iterrows():
			kwargs = {}
			for x, y in v.items():
				kwargs[x] = y
			self.D.add_to_devices(what=dic, **kwargs)

		u_df = device_df_drop_empty_duplicates(dic)
		return u_df



# --------------------------------------------- 

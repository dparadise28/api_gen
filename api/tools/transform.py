import locale, json, os, datetime, functools
from copy     import deepcopy
from protocol import method_map
#from   mobile.proc_common import decrypt_password

config  = {}
#locale.setlocale( locale.LC_ALL, 'en_US.UTF-8')

class Remodeler:
	def __init__(self, configs):
		global config
		config = deepcopy(configs)


	def remodel_flat_dict(self, original, template):
		'''
			configures api input arguments:

				original = inputs by user to be remapped with 
				template = key or key list to mapping dict

					eg:
					flat
						config: {
							template_desired: {
								new_key_1: old_key_1,
								new_key_1: old_key_2,
								...
							},
							map_i: {
								new_key_1: old_key_1,
								new_key_2: old_key_2,
								...
							},
							...
						}# template = template_desired or touple(template_desired)

					nested:

						config: {
							templates: {
								map1: {
									new_key_1: old_key_1,
									new_key_1: old_key_2,
									...
								}, map2: {
									new_key_1: old_key_1,
									new_key_1: old_key_2,
									...
								},
								...
								, template_desired: {
									new_key_1: old_key_1,
									new_key_1: old_key_2,
									...
								}, #config you need
								...
							}
						}# in this case template = (templates, template_desired)
		'''
		expected = deepcopy(config[template] if type(template) == str else self.retrieve(template, config, template))
		for key in expected:
			if type(expected[key]) == dict and expected[key].get('value', '') in original:
				expected[key] = self.format_val(original[expected[key]['value']], key)
			elif key in original:
				expected[key] = self.format_val(original[key], key)
			else:
				expected[key] = self.format_val('', key)
		return expected


	def retrieve(self, key_list, resp, ret_key, skip = False):
		'''
			retrieves a value from an arbitratily nested dict. the value returned will
			either be any valid field a dict/json object acceps, or false if no value
			was found given the dictionary and key list specified.

			inputs:
				key_list = tuple or list of keys used to traverse the dict
						   holding the desired value

				resp     = dict holding desired value

				ret_key  = key name for specific value to be returned for formatting purposes
		'''
		val = '' if not skip else resp
		try:
			val = functools.reduce(lambda d, k: d[k], key_list, resp)
			return self.format_val(val, ret_key)
		except:
			return self.format_val(val, ret_key)


	def remodel_nested_dict(self, resp, ret, key = ''):
		'''
			This methos constructs the expected response the app is expecting
			(however flat or nested they may be)

			NOTE: It is highly dependant on the configuration setup

			inputs:
				resp = response from the api. Given the recursive nature of this
					   implementation this value will first be the full response
					   from the api; if the configuration calls for a list it will
					   retrieve a subset of the results to iterate through as multiple
					   values will be required for that response.
		'''
		configed_ret = deepcopy(ret)
		for result in ret:
			if type(result) == tuple:
				configed_ret += [self.retrieve(result, val, key) for val in resp]
			elif type(ret[result]) == tuple:
				configed_ret[result] = self.retrieve(configed_ret[result], resp, result)
			elif type(ret[result]) == dict:
				configed_ret[result] = self.remodel_nested_dict(resp, configed_ret[result], result)
				if config.has_key('resp_structure_change'):
					if config['resp_structure_change'].has_key(result):
						configed_ret[result] = self.retrieve(['fail'], configed_ret[result], result, True)
			elif type(ret[result]) == list:
				temp, loop_through = [], config['loop_through_vals']
				for val in ret[result]:
					temp += [self.retrieve(val, val_in_list, result) if type(val) == tuple else self.remodel_nested_dict(val_in_list, val, result)
							 for val_in_list in self.retrieve(loop_through[result], resp, '')]
				configed_ret[result] = temp

		return configed_ret


	def format_val(self, val, key):
		'''
			val    = value to be formated if needed
			key    = key in the val_format dict to specify if and how the value
					 needs formating
		'''
		if 'val_format' in config:
			fmat = config['val_format']
			boolean = {
				'SUCCESS': True,  'true' : True,  'True' : True,  'TRUE' : True,  '1': True,  1: True,  True : True,
				'FAILED' : False, 'false': False, 'False': False, 'FALSE': False, '0': False, 0: False, False: False,
			}
			if key in fmat:
				if type(fmat[key]) == str:
					val = method_map[fmat[key]](val)
					'''
						REFACTOR
							move to protocol (map by format key and have val as a consistent input)
							--allows for more flexibility and consistent sustainable code reuse
					'''
					# if   fmat[key]       == 'currency'      : val = locale.currency(float(val) if (val != '' and '$' not in val and not any(char.isalpha() for char in str(val))) else 0.0)
					# elif fmat[key]       == 'neg_currency'  : val = '-{0}'.format(locale.currency(float(val) if val != '' else 0.0))
					# elif fmat[key]       == 'FreeOrCurrency': val = '{0}'.format(locale.currency(float(val))) if '0.0' not in str(val) and val else 'FREE'
					# elif fmat[key]       == 'str'           : val = str(val)
					# elif fmat[key]       == 'd2l'           : val = val.values() 
					# elif fmat[key]       == 'dk2l'          : val = sum([promo.keys() for promo in val], []) if type(val) == list else []
					# elif fmat[key]       == 'boolean'       : val = boolean[val] if val in boolean.keys() else val
					# elif fmat[key]       == 'promo'         : val = [{'name': promo, 'message': ''} for promo in val]
					# elif fmat[key]       == 'int2date'      : val = datetime.datetime.utcfromtimestamp(int(str(val if val != '' else 0)[0:10])).strftime('%m/%d/%Y')
					# elif type(fmat[key]) == dict            : val = fmat[key][val] if fmat[key].has_key(val) else val
					#elif fmat[key]       == 'decrypt'       :
					#    try   : val = decrypt_password(val)
					#    except: pass
				else:
					''' to be determined (more definition needed)'''
					for action in fmat[key]:
						if action[0] == 'strip':
							for bad in action[1]:
								val = val.replace(bad, '')
						elif action[0] == 'int2date'  : val = datetime.datetime.utcfromtimestamp(int(str(val if val != '' else 0)[0:10])).strftime('%m/%d/%Y')
						elif action[0] == 'insert_val': val = action[1].format(val)
						elif action[0] == 'replace'   : val = action[1]
		return val
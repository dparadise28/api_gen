from copy import deepcopy

d={
	"activation_code": "",
	"date_created"   : "",
	"subscribed"     : "",
	"first_name"     : "",
	"last_name"      : "",
	"user_name"      : "index",
	"activated"      : "", #if not activated account will expire 24 hrs after creation date (to be implemented)
	"status"         : "",
	"phone"          : "",
	"email"          : "index",
	"desc"           : "",
	"items": [{
		"poster_id": "", #id of the user that posted this "thing"
		"post_date": "",
		"end_date" : "",
		"image"    : "",
		"price"    : "",
		"type"     : "",
		"name"     : "",
	}],
	"order": {
		"estimated_order_total": "",
		"order_subtotal"       : "",
		"estimated_tax"        : "",
		"order_number"         : "",
		"order_total"          : "",
		"sales_tax"            : "",
		"order_history"        : [{
			"billing_last_name": "",
			"billing_zip_code" : "",
			"tracking_urls"    : "",
			"order_status"     : "",
			"order_code"       : "",
			"order_date"       : "",
			"order_number"     : "",
			"cart"             : [{
				"poster_id": "index", #id of the user that posted
				"post_date": "",
				"end_date" : "index",
				"state"    : "index",
				"image"    : "",
				"price"    : "index",
				"type"     : "",
				"name"     : "index",
			}],    #list of thing ids
		}], #list of transaction ids
	},
}


import json

def unpack(nested_dict, dict_name = 'main'):
	'''
		unpacks nested dicts
		
		example:
			nested_dict = {
				"1": "1",
				"2": {
					"2": ["4"]
				},
				"3": [{
					"1": "1",
					"3": [{
							"1": "1"
						}]
				}]
			}

		return:
			[
				{
					"main": {"2": {}, "1": "1", "3": []}
				},{
					"3": {"1": "1","3": []}
				},{
					"3": {"1": "1"}
				},{
					"2": {"2": ["4"]}
				}
			]
	'''
	extracted_lists = []
	def unpacked(r, key): #todo: reference to parent in dicts, removal of duplicates
		nonlocal extracted_lists
		def l(k, v):
			if isinstance(v[0], dict): extracted_dict.update({k: []}); unpacked(v[0], k)
			else: extracted_dict.update({k: v})
		def d(k, v): extracted_dict.update({k: unpacked(v, k)})
		def s(k, v): extracted_dict.update({k: v})

		protocol, extracted_dict = {list: l, dict: d, str : s,}, {}

		for k,v in r.items():
			protocol[type(v)](k, v)
		extracted_lists.append({key: extracted_dict}); return {}
	unpacked(nested_dict, dict_name); return list(reversed(extracted_lists))
print(json.dumps(unpack({
				"1": "1",
				"2": {
					"2": ["4"]
				},
				"3": [{
					"1": "1",
					"3": [{
							"1": "1"
						}]
				}]
			}, 'main'), indent = 4))
# return unpacked(nested_dict, dict_name)
# print(json.dumps(unpack(d), indent = 4))
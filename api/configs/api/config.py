from configs.api.generic_response import response
from configs.api.r_queries          import create_account, activate_account, browse_tree, update_browse_tree

from protocol import method_map

generic_arg = {
	'type'      : str,
	'encrypted' : True,
	'conditions': {},
	'formatting': {},
}
args = {
	'first_name'         : generic_arg,
	'last_name'          : generic_arg,
	'user_name'          : generic_arg,
	'user_id'            : generic_arg,
	'email'              : generic_arg,
	'password'           : generic_arg,
	'verify_pw'          : generic_arg,
	'activation_code'    : generic_arg,
	'new_activation_code': generic_arg,
}

api = {
	'val_format': {
		'new_activation_code': 'generate_code',
	},

	'ret': response,
	'args': args,
	'calls': {
		'create_account': {
			'required_args': [],
			'optional_args': [],
			'actions': [{
				'type'    : 'query',
				'query'   : create_account, #change to key and not actual query to further abstract db
				'required': True
			}, {
				'type'  : 'email_activation_code',
				'email_activation_code': method_map['email_activation_code'],
			}]
		},
		
		'activate_account': {
			'required_args': [],
			'optional_args': [],
			'actions': [{
				'type' : 'query',
				'query': activate_account,
			}]
		},
		
		'browse_tree': {
			'required_args': [],
			'optional_args': [],
			'actions': [{
				'type' : 'query',
				'query': browse_tree,
			}]
		},
	},
}
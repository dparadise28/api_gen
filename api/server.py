from copy import deepcopy
import cherrypy, json, protocol

class Server():
	def __init__(self, base_server, api_conf, remodeler, connection_pool):
		self.base = deepcopy(base_server)
		self.fetch = lambda orig, config, arg: remodeler(config).remodel_flat_dict(orig, arg)
		self.api_conf = api_conf
		self.connection_pool = connection_pool

		self.query_path = lambda api_call: ('calls', api_call, 'query',)
		self.actions_path = lambda api_call: ('calls', api_call, 'actions',)
		self.generic_args_path = ('args',)
		self.required_args_path = lambda api_call: ('calls', api_call, 'required_args',)
		self.optional_args_path = lambda api_call: ('calls', api_call, 'optional_args',)

	@cherrypy.expose()
	@cherrypy.tools.json_out()
	def generic_call(self, *args, json_body = False):		
		if cherrypy.request.body.length:
			data = cherrypy.request.json; json_body = True
			cherrypy.log('body')
			cherrypy.log(json.dumps(data))
		#response = deepcopy(self.api_conf['ret'])
		
		cherrypy.log('args')
		cherrypy.log(json.dumps(args))
		
		req = self.fetch(data, self.api_conf, self.generic_args_path) if json_body else {}
		#cherrypy.log(json.dumps(req))
		print(req)
		actions = self.api_conf['calls'][args[0]]['actions']
		action_returns = []
		for action in actions:
			#for initial testing only(need to map)
			if action['type'] == 'query':
				result = self.connection_pool().execute(action['query'], req)
				action_return = result
			else:
				print(action[action['type']], str(action[action['type']]))
				action_return = action[action['type']](req)
			action_returns.append(action_return)
			print('\n\n\n\n')
			print(action_returns)
			if action.get('required') and action_returns[-1].get('status') == 'Failed':
				return action_returns[-1]
		return result

	def generate(self):
		#get
		setattr(self.base, 'api', self.generic_call)
		#post
		setattr(self.base, 'api', cherrypy.tools.json_in()(self.generic_call))
		return self.base
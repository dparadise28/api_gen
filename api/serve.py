#kind of a hack but better solutions can be explored later
import sys
sys.path.append('..')

from data_center.rethinkdb_pool   import ConnectionManager
from configs.api.cp_config import conf
from configs.api.config    import api
from tools.transform       import Remodeler
from server                import Server
from copy                  import deepcopy
import cherrypy

class BaseServer(object):
	'''
		base server used as a shell to be dynamically populated 
		with attribute

		Each attribute definition is identically generic and configurable
		thus allowing for dynamic api generation
	'''
	def __init__(self):
		# self.Remodeler = Remodeler
		# self.conf = conf
		# self.api = api
		pass

if __name__ == '__main__':
	'''
		launching app using cp quickstart 

		inputs:
			cherrypy.quickstart:
				1) Server - application to be  served by cherry's wsgi server

					1) BaseServer- server shell (read the above for further information)

					2) api       - config file that dictates the requirements and behaviour
							       of the api (like a dispatcher protocol in a sense)

					3) Remodeler - transformation tool (for more information please see the
								   documentation provided in the tool itself)

				2)config - config file for cherrypy server
	'''
	cherrypy.quickstart(Server(BaseServer, api, Remodeler, ConnectionManager).generate(), config = conf)
# from data_center.rethinkdb_pool import ConnectionManager
import rethinkdb as r

class ConnectionManager():
	def __init__(self):
		try:
			#self.pool = ConnectionPool(db='ecom')
			self.conn = r.connect()#pool.acquire()
		except:
			print("I am unable to connect to the database")

	def get_con(self):
		return self.con.getconn()

	def execute(self, query, args):
		result = query(args, self.conn)
		return resul

def spin_up(structure):
	con = connection_pool()
	
spin_up({})
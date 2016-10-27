from repool import ConnectionPool
import rethinkdb as r

class ConnectionManager():
	def __init__(self):
		try:
			#self.pool = ConnectionPool(db='ecom')
			self.conn = r.connect(db='ecom')#pool.acquire()
		except:
			print("I am unable to connect to the database")

	def get_con(self):
		return self.con.getconn()

	def execute(self, query, args):
		result = query(args, self.conn)
		return result
from psycopg2 import pool, DatabaseError

class ConnectionManager():
	def __init__(self):
		try:
			self.con = pool.ThreadedConnectionPool(5, 100, database='db_v1', user='postgres', password='dag102864')
		except:
			print("I am unable to connect to the database")

	def get_con(self):
		return self.con.getconn()

	def execute(self, query, args):
		with self.get_con() as con:
			with con.cursor() as cur:
				try:
					cur.execute(query, args); result = cur.fetchall(); con.commit()
				except DatabaseError as e:
					if con:
						con.rollback()
					result = [[{"status": "Failed", "error": "{}".format(e)}]]
			self.con.putconn(con)
		return result[0][0]
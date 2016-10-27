from repool import ConnectionPool
import rethinkdb as r
import time

# pool = ConnectionPool(db='rethinkvsmongo')
# conn = pool.acquire()

conn = r.connect(db='rethinkvsmongo')
metrics_document = {
    "table_name" : "django_session",
    "cumulative_pct_reads" : 69.859,
    "cache_hit_rate" : 90.2000000000000028,
    "last_update" : '',
    "reads" : 51,
    "index_hit_rate" : 37.5,
    "size" : 1
}

try:
	r.db_create('rethinkvsmongo').run(conn)
	r.db('rethinkvsmongo').table_create('metrics').run(conn)
	r.table('metrics').index_create('last_update').run(conn)
except:
	pass

start_time = time.time()
total_time = 0
unix_timestamp = 0
print('starting ...\n\n')
for i in range(0, 100000):
	metrics_document['last_update'] = unix_timestamp+i
	check = False
	while not check:
		try:
			r.table('metrics').insert(metrics_document, durability='soft').run(conn) #changed from hard to soft
			check = True
		except:
			check = False
		# finally:
			# pool.release(conn)
	if i % 1000 == 0:
		total_time = total_time + (time.time() - start_time)
		time_diff = time.time() - start_time
		start_time = time.time()
		print('# of inserts: ', i, '\t\t 1k batch time: ', time_diff, '\t\t total time spent so far: ', total_time)
		# if i % 3000 == 0:
			# print('\n\n\trestarting connection')
			# conn.close()
			# conn = r.connect(db='rethinkvsmongo')
			# print('\t\trestarted\n\n')
# pool.release_pool()
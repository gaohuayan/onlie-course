import redis

r1 = redis.Redis(db=0)
print(r1.get('myKey'))

pool = redis.ConnectionPool(max_connections=10,db=0)
r2 = redis.Redis(connection_pool=pool)

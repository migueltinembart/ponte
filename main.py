from testcontainers.redis import RedisContainer
from testcontainers.core.container import wait_for_logs
import json
## DOCKER_HOST=unix:///Users/$USER/.colima/default/docker.sock;
## TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock

redis = RedisContainer("redis:latest")
redis.start()

wait_for_logs(redis, "Ready to accept connections")

rc = redis.get_client(decode_responses=True)

rc.set("string", "value")
rc.set("objectstring", '{"json": true}')

print(rc.get("string"))
print(rc.get("objectstring"))
test = json.loads(str(rc.get("objectstring")))
print(test)

rc.set("instance:1", "test")
rc.set("instance:2", "jest")

pattern = "instance:*"

cursor = "0"
keys=[]
while cursor != 0:
        cursor, scanned_keys = rc.scan(cursor=cursor, match=pattern, count=100) # type: ignore
        keys.extend(scanned_keys)

print(keys)

values = rc.mget(keys)

print(values)

rc.hset("user:1",mapping={'name': "test", 'age': 5})
rc.hset("user:2",mapping={'name': "jest", 'age': 6})

pattern = "user:*"

cursor = "0"
keys=[]
while cursor != 0:
    cursor, scanned_key_value = rc.scan(cursor=cursor, match=pattern, count=1)
    keys.extend(scanned_key_value)

print(keys)

pipe = rc.pipeline()
for key in keys:
    pipe.hgetall(key)

maps = pipe.execute()

print(maps)
print(type(maps))
redis.stop()

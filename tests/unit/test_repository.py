import sys
import os

# Get the absolute path to the src directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Add src_path to sys.path
sys.path.append(src_path)

import pytest
import logging
from testcontainers import redis
from testcontainers.core.container import wait_for_logs
from store.redis import Book, RedisRepository

redisContainer = redis.RedisContainer("redis:7.4.1")

@pytest.fixture(scope="session", autouse=True)
def session(request: pytest.FixtureRequest):
    logging.info("[fixture] starting redis container")

    redisContainer.start()

    wait_for_logs(redisContainer, "Ready to accept connections")

    def stop_redis():
        logging.info("[fixture] Stoping redis container")
        redisContainer.stop()

    request.addfinalizer(stop_redis)
    
    rc = redisContainer.get_client(decode_responses=True)

    rc.set("book", '{"test": "test" e}')

def test_repo():
    rc = redisContainer.get_client(decode_responses=True)
    book = Book(name="", pages=2, author="test")
    bookRepo = RedisRepository[Book](rc=rc, key="book", model=book)
    rc.hset("book:1", mapping={'name': "the book", 'pages': 200, 'author': "Miguel"})
    list = bookRepo.list()
    logging.info("test__", list)
    assert len(list) == 1

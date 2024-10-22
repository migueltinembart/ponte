import sys
import os
from typing import List

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.append(src_path)

from _pytest.monkeypatch import resolve
import pytest
import logging
from testcontainers import redis
from testcontainers.core.container import wait_for_logs
from store.redis import Book, RedisRepository

# Prefect

redisContainer = redis.RedisContainer("redis:7.4.1")


def setup():
    rc = redisContainer.get_client(decode_responses=True)

    books: List[Book] = []

    book_one = Book(name="Miguels Book", pages=200, author="Miguel")
    book_two = Book(name="Nanas Book", pages=3000, author="Someone")
    # Initialize the database manually for better testing
    books.append(book_one)
    books.append(book_two)

    for book in books:
        count = rc.incr("book_id")
        rc.hset("book:{}".format(str(count)), mapping=dict(book))


@pytest.fixture(scope="session", autouse=True)
def session(request: pytest.FixtureRequest):
    logging.info("[fixture] starting redis container")

    redisContainer.start()

    wait_for_logs(redisContainer, "Ready to accept connections")

    def stop_redis():
        logging.info("[fixture] Stoping redis container")
        redisContainer.stop()

    request.addfinalizer(stop_redis)

    setup()


def test_if_list_is_initialized_with_books():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    assert len(bookRepo.list()) == 2

def test_if_keys_are_correctly_defined():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    bookRepo.delete(1)
    assert len(bookRepo.list()) == 1

def test_if_hashmaps_can_be_created():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    
    book = Book(name="Harry Potter", pages=600, author="J.K. Rowling")
    bookRepo.create(book)
    
    result = bookRepo.list()
    print(result)
    assert len(result) == 2
    assert isinstance(result[1], Book)

def test_if_getting_Book_is_actually_a_Book():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    
    result = bookRepo.get(2)
    
    assert isinstance(result, Book)


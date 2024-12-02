import sys
import os
from typing import List

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
sys.path.append(src_path)

from pydantic import BaseModel
import pytest
import logging
from testcontainers import redis
from testcontainers.core.container import wait_for_logs
from store.redis import RedisRepository

# Test class
class Book(BaseModel):
    name: str
    pages: int
    author: str

# Prefect

redisContainer = redis.RedisContainer("redis:7.4.1")

def setup():
    '''sets up a simple dataset for tests'''
    rc = redisContainer.get_client(decode_responses=True)

    books: List[Book] = []

    book_one = Book(name="Miguels Book", pages=200, author="Miguel")
    book_two = Book(name="Nanas Book", pages=3000, author="Someone")
    # Initialize the database manually for better testing
    books.append(book_one)
    books.append(book_two)

    for book in books:
        count = rc.incr("bookcounter")
        rc.hset("book:{}".format(str(count)), mapping=dict(book))

# Fixture gets run before the tests to initialize redis container
# autouse makes the fixture automatically attach to the test
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

def test_if_keys_are_there():
    rc = redisContainer.get_client(decode_responses=True)
    
    entries = []
    for i in range(2):
        entries.append(rc.hgetall(f"book:{i}"))
    
    keys = rc.keys(f"book:*")
    
    id = rc.get("bookcounter")

    assert len(entries) == 2
    assert len(keys) == 2
    assert id == "2"

def test_if_list_is_initialized_with_books():
    rc = redisContainer.get_client(decode_responses=True)
    
    result = rc.hgetall("book:1")
    book1 = Book.model_validate(result)

    assert isinstance(book1, Book)
    assert book1.name == "Miguels Book"
    assert book1.pages == 200
    assert book1.author == "Miguel"

def test_repository_returning_list_of_books():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")

    result = bookRepo.list()

    assert len(result) == 2 
    assert isinstance(result, List)
    assert isinstance(result[1], Book)

def test_repository_creating_Book():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    
    book = Book(name="Harry Potter", pages=600, author="J.K. Rowling")
    created = bookRepo.create(book) 

    result = bookRepo.list()
    assert created == True
    assert len(result) == 3
    assert isinstance(result[2], Book)

def test_removing_key():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    result = bookRepo.delete(2)
    result2 = bookRepo.delete(2)  
    listresult = bookRepo.list()

    assert result == True
    assert result2 == False
    assert len(listresult) == 2

def test_if_deleted_keys_will_not_be_reassigned():
    previosly_deleted_id = 2
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")
    book = Book(name="Schneewitchen", pages=100, author="Irgendjemand")
    
    bookRepo.create(book)

    not_exist = bookRepo.get(previosly_deleted_id)
    exist = bookRepo.get(4)

    assert not_exist == None
    assert isinstance(exist, Book)

def test_repository_updates_correct_record():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")

    to_change = 3 
    
    old = bookRepo.get(to_change)
    book = Book(name=old.name, author=old.author, pages=10000)
    result = bookRepo.update(to_change, book)
    new = bookRepo.get(to_change)

    assert old != new
    assert new.pages == 10000
    assert result == True


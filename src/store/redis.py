from typing import Generic, List, Type, TypeVar
from pydantic import BaseModel
from redis import Redis
from testcontainers.core.utils import logging
from store.definitions import  Repository
from typing import Optional, Any
import json

DataT = TypeVar("DataT")


class Book(BaseModel):
    name: str
    pages: int
    author: str

def redis_response_to_pydantic_model(response: Any, model: BaseModel) -> Optional[BaseModel | List[BaseModel] | None]:
    print(response)
    if response is None:
        return None
    if isinstance(response, bytes):
        print("Was bytes")
        response = response.decode('utf-8')
    if isinstance(response, str):
        print("Was string")
        data_dict = json.loads(response)
        return model.model_validate(**data_dict)
    elif isinstance(response, dict):
        print("was dict")
        # Convert keys and values from bytes to strings if necessary
        data_dict = {
            (k.decode('utf-8') if isinstance(k, bytes) else k):
            (v.decode('utf-8') if isinstance(v, bytes) else v)
            for k, v in response.items()
        }
        return model.model_validate(**data_dict)
    elif isinstance(response, list):
        # Handle list of models
        item_list = []
        for item in response:
            item_list.append(redis_response_to_pydantic_model(item, model_class))
        return item_list
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")

class RedisRepository[T: BaseModel](Repository): 
    """Defines A model, wich takes a redis client as dependency"""
    def __init__(self, rc: Redis, key: str, model: T ) -> None:
        super().__init__()
        self.__rc: Redis = rc
        self.__key: str = key
        self.__model: T = model

    def list(self, options=None):
        if options:
            pass
        
        with self.__rc as rc:
            cursor = "0"
            limit=100
            pattern="{}:*".format(self.__key)
            key_list=[]
            while cursor != 0:
                cursor, keys = rc.scan(cursor=cursor, match=pattern, count=limit) # type: ignore
                key_list.extend(keys)
               
            pipe = rc.pipeline()
            for key in key_list:
                pipe.hgetall(key)
            result = pipe.execute()
                                  
        return redis_response_to_pydantic_model(result, type(self.__model))


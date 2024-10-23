from typing import List,Union, get_args 
from pluggy import Result
from pydantic import BaseModel
from redis import Redis
from typing import  Any
import json

class Book(BaseModel):
    name: str
    pages: int
    author: str

def fromStr[T: BaseModel](response: Any, model: T) -> Union[T, None]:
    if response is None:
        return None
    if isinstance(response, str):
        data_dict = json.loads(response)
        return model.model_validate(**data_dict)
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")
    

def fromDict[T: BaseModel](response: Any, model: T) -> Union[T, None]:
    if response is None:
        return None
    if isinstance(response, dict):
        # Convert keys and values from bytes to strings if necessary
        data_dict = {
            (k.decode("utf-8") if isinstance(k, bytes) else k): (
                v.decode("utf-8") if isinstance(v, bytes) else v
            )
            for k, v in response.items()
        }
        return model.model_validate(data_dict)
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")


def redis_response_to_pydantic_model[T: BaseModel](
    response: Any, model: T
) -> Union[List[T] ,T , None]:
    if response is None:
        return None
    if isinstance(response, bytes):
        response = response.decode("utf-8")
    if isinstance(response, str):
        data_dict = json.loads(response)
        return model.model_validate({**data_dict})
    elif isinstance(response, dict):
        # Convert keys and values from bytes to strings if necessary
        data_dict = {
            (k.decode("utf-8") if isinstance(k, bytes) else k): (
                v.decode("utf-8") if isinstance(v, bytes) else v
            )
            for k, v in response.items()
        }
        return model.model_validate({**data_dict})
    elif isinstance(response, list):
        # Handle list of models
        item_list = []
        for item in response:
            item_list.append(redis_response_to_pydantic_model(item, model))
        return item_list
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")


class RedisRepository[T: BaseModel]:
    """Defines A model, wich takes a redis client as dependency"""

    def __init__(self, rc: Redis, key: str) -> None:
        self.__rc: Redis = rc
        self.__key = key

    def list(self, options=None) -> List[T] | None:
        if options:
            pass

        with self.__rc as rc:
            cursor = "0"
            limit = 100
            pattern = f"{self.__key}:*"
            key_list = []
            while cursor != 0:
                cursor, keys = rc.scan(cursor=cursor, match=pattern, count=limit)  # type: ignore
                key_list.extend(keys)
            pipe = rc.pipeline()
            for key in key_list:
                pipe.hgetall(key)
            result = pipe.execute()
        

        data_model = get_args(self.__orig_class__)[0] # type: ignore

        return redis_response_to_pydantic_model(result, data_model)
    
    def get(self, id: int, options=None) -> T | None:
        if options:
            pass
        full_key = f"{self.__key}:{id}"
        with self.__rc as rc:
            result = rc.hgetall(full_key) 
        if not result:
            return None
        data_model = get_args(self.__orig_class__)[0] # type: ignore

        return fromDict(result, data_model)

    def create(self, model: BaseModel, options=None) -> bool:
        if options:
            pass

        with self.__rc as rc:
            print("key is", self.__key)
            current_id = f"{self.__key}counter"
            count = rc.incr(current_id)
            
            with rc.pipeline() as pipe:

                pipe.hset(f"{self.__key}:{count}", mapping=dict(model))
                result = pipe.execute()
            print("pip result:", result)
            print(model.model_fields.keys())
            if result[0] == len(model.model_fields.keys()):
                return True

            return False

    def update(self, id: int, model: BaseModel, options=None) -> bool:
        if options:
            pass

        with self.__rc as rc:
            result = rc.hset(f"{self.__key}:{id}", mapping=dict(model))
        
        if result == 0:
            return True
        return False

    def delete(self, id: int, options=None) -> bool:
        if options:
            pass


        with self.__rc as rc:
            result = rc.delete(f"{self.__key}:{id}")

            if result == 1:
                return True

        return False

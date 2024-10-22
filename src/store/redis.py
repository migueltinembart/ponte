from typing import List, TypeVar, get_args, Generic
from pydantic import BaseModel
from redis import Redis
from store.definitions import Repository
from typing import Optional, Any
import json

DataT = TypeVar("DataT")


class Book(BaseModel):
    name: str
    pages: int
    author: str


def redis_response_to_pydantic_model(
    response: Any, model: BaseModel
) -> Optional[BaseModel | List[BaseModel] | None]:
    if response is None:
        return None
    if isinstance(response, bytes):
        response = response.decode("utf-8")
    if isinstance(response, str):
        data_dict = json.loads(response)
        return model.model_validate(**data_dict)
    elif isinstance(response, dict):
        # Convert keys and values from bytes to strings if necessary
        data_dict = {
            (k.decode("utf-8") if isinstance(k, bytes) else k): (
                v.decode("utf-8") if isinstance(v, bytes) else v
            )
            for k, v in response.items()
        }
        return model.model_validate(data_dict)
    elif isinstance(response, list):
        # Handle list of models
        item_list = []
        for item in response:
            item_list.append(redis_response_to_pydantic_model(item, model))
        return item_list
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")

T = TypeVar('T', bound=BaseModel)

class RedisRepository(Generic[T]):
    """Defines A model, wich takes a redis client as dependency"""

    def __init__(self, rc: Redis, key: str) -> None:
        super().__init__()
        self.__rc: Redis = rc
        self.__key: str = key

    def list(self, options=None) :
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
        return redis_response_to_pydantic_model(result, data_model) # type: ignore

    def get(self, id: int, options=None):
        if options:
            pass
        full_key = ":".join((self.__key, str(id)))
        with self.__rc as rc:
            result = rc.hgetall(full_key)

        data_model = get_args(self.__orig_class__)[0] # type: ignore
        return redis_response_to_pydantic_model(result, data_model)

    def create(self, model: BaseModel, options=None):
        if options:
            pass

        with self.__rc as rc:
            pipe = rc.pipeline()
            current_id = f"{self.__key}_id"

            count = pipe.incr(current_id)
             
            pipe.hset(f"{self.__key}:{count}", mapping=dict(model))

            result = pipe.execute()

        match result:
            case 0:
                return False
            case 1:
                return True

    def update(self, id: int, model: BaseModel, options=None):
        if options:
            pass


        with self.__rc as rc:
            pipe = rc.pipeline()
            pipe.hset(f"{self.__key}_{id}", mapping=dict(model))

            result = pipe.execute()

        model_class = get_args(self.__orig_class__)[0] # type: ignore

        return redis_response_to_pydantic_model(result[0], model_class)

    def delete(self, id: int, options=None):
        if options:
            pass


        with self.__rc as rc:
            result = rc.delete(f"{self.__key}:{id}")

        match result:
            case 0:
                return False
            case 1:
                return True

---
title: Snippets
date: 2024-01-19
tags: 
    - code 
    - python
    - generics
---

# Snippets

Wenn es sich ergibt ein Design Pattern generisch zu schreiben, versuche ich das auch zu tun. Sonst versuche ich die Implementation nahe an der Quellstruktur zu halten, ehe es sich lohnen würde arbeit in wiederverwendbaren Code zu schreiben wenn nur ein Objekt dann von einer abstrakten Klasse erbt. Dies verursacht eine Suche nach Perfektion wo die Grundidee noch nicht vollständig erkundigt ist und nicht jegliche male eingesetzt ist worden.

Darum stelle ich hier Code Snippets zur Verfügung welche ich als Wichtig für die Umsetzung des Projekts empfunden habe, da die mir Blockaden auf meinem Weg genommen haben, welche ich manchmal mehrere male neu erfinden musste.

## Repository Pattern

Das Repository Pattern ist der Grundbaustein um Daten auf der Redisdatenbank aufsetzen zu können. Somit mussten die Grundoperationen mit einer generischen Klasse erstellt werden. Vererbung hätte hier auch geklappt um eine abstrakte  Klasse zu erstellen, ich finde aber wenn man mit einer Datenstruktur arbeiten kann, erwartet man wenn möglich gerne einen bestimmten Typ zurück und mit generischen Funktionen kann das Pattern umstandsloser eingesetzt werden.

> [!IMPORTANT]
> Die Syntax die hier verwendet wird ist erst ab Python 3.12 möglich. 

```python
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
                cursor, keys = rc.scan(cursor=cursor, match=pattern, count=limit)
                key_list.extend(keys)
            pipe = rc.pipeline()
            for key in key_list:
                pipe.hgetall(key)
            result = pipe.execute()
        

        data_model = get_args(self.__orig_class__)[0]

        return redis_response_to_pydantic_model(result, data_model)
    
    def get(self, id: int, options=None) -> T | None:
        if options:
            pass
        full_key = f"{self.__key}:{id}"
        with self.__rc as rc:
            result = rc.hgetall(full_key) 
        if not result:
            return None
        data_model = get_args(self.__orig_class__)[0]

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

def redisRepositoryFactory[T: BaseModel](key: str) -> RedisRepository:

    return RedisRepository[T](
        rc=Redis(),
        key=key
    )
```

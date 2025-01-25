--
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

Dies erlaubt mir den Typ `T` durch einen beliebigen Typ zu ersetzen und meine Typendeklarationen erwarten immer den entsprechenden Typ von Redis. Redis behält durch den key den Überblick und weiss wo die entsprechenden Daten abgelegt sind.

## externen Output validieren

Beim holen oder erstellen von VMs mit der Azure SDK für Python möchte ich dass die von mir festgelegten Felder einer Azure VM Definition entsprechen und muss dementsprechend den Input durch pydantic validieren lassen indem ich mit der walrus notation alle Werte auf ihre Präsenz überprüfe, da man bei einem API Aufruf auch davon ausgehen könnte das bestimmte Felder undefiniert sind.

```python
class AzureStorageConfig(BaseModel):
    type: Literal["primary", "data"]
    size: int
    disk_type: Literal["Standard_LRS", "Premium_LRS", "StandardSSD_LRS", "UltraSSD_LRS", "Premium_ZRS", "StandardSSD_ZRS", "PremiumV2_LRS"]
```

Dies entspricht dem Model welches in yaml in der `ponte` configuration eingetragen ist. Bevor die VM erstellt wird, muss diese gegenüber Azure geprüft werden ob sich nichts am File verändert hat. So muss ponte keine Veränderungen vornehmen. Sobald aber die Konfiguration beim Storage angepasst werden müsste, müsste die VM zerstört und entsprechend der neuen Konfiguration erstellt werden.

```python
def getAzureVMStorageConfig(vm: VirtualMachine) -> List[AzureStorageConfig]:
    disks: List[AzureStorageConfig] = []
    secondary_disks: List[AzureStorageConfig] = []
    
    if (storage_profile := vm.storage_profile):
        if (os_disk := storage_profile.os_disk) and (disk_size_gb := os_disk.disk_size_gb) and ( managed_disk := os_disk.managed_disk ) and (storage_account_type := managed_disk.storage_account_type):
            if storage_account_type is str:
                primary_disk = AzureStorageConfig(
                    type="primary", 
                    size=disk_size_gb,
                    disk_type=storage_account_type
                )
                disks.append(primary_disk)
        else:
            raise ValidationError("No os Disk found for virtual machine")

        if (data_disks := storage_profile.data_disks):
            for disk in data_disks:
                if (disk_size_gb := disk.disk_size_gb) and (managed_disk := disk.managed_disk) and (storage_account_type := managed_disk.storage_account_type):
                    secondary_disks.append(AzureStorageConfig(type="data", size=disk_size_gb, disk_type=storage_account_type)) # type: ignore
    
        disks.extend(secondary_disks)
    else:
        raise ValueError("Storage profile could not be read from virtual machine")

    return disks
```

Die Verkettung von And Operationen ermöglichst es mir eine Operation als ganzes anzusehen. alle Felder die nicht optional sind werden nicht geprüft und am Ende validiert das `AzureStorageConfig`. Beim aufrufen der Funktion werden die möglichen Validationsfehler gecatcht und markieren das Deployment als Fehlschlag.

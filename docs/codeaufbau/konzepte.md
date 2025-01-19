---
title: Konzepte
date: 2025-01-18
tags:
    - test
---

# Konzepte

Um den Aufbau von Ponte besser erklären zu können, versuche ich hier einzelne Konzepte und Zeichnungen zu verfassen, die und Komponenten festlegt. 

## Event Driven

Ponte versucht Event Driven zu agieren in dem es Events in Form von Webhooks abfangen möchte um dabei herauszufinden, was für ein Event getriggert wurde. Events können bei verschiedenen Plattformen anders sein, bei Github können Applikationen auf einer per Repository Basis oder auf einer per Applikations-Basis feingestimmte Trigger für Events setzen. Beispiele solcher Events sind:

- Ein Push auf den `Main` Branch
- Ein eröffneter Pull Request
- Ein Issue eröffnen
- Bei einem Github Action

Dabei sendet Github einen HTTP Post-Request mit einem bestimmten Payload im Body in Form von `json`. Die Dokumentation von Github zeigt alle Event Payloads mit der Dokumentation der einzelnen Felder und deren Typenbezeichnung. So kann der Entwickler dieses Schema zur Validierung benutzen um mit den Daten sinnvolle Klassen und Objekte zu erstellen und kann sich sicher sein, dass jedes Feld und aber auch verschachtelte Objekte in valide Datenformen umgesetzt werden können. 

### Datenvalidierung mit Pydantic

Für die Validierung aber auch für die Instanzierung von Datenbezogennen Klassen für Repository Patterns, wird [Pydantic](https://docs.pydantic.dev/latest) verwendet. Pydantic bietet ein sinnvolles Basismodel, in Python `BaseModel`, welches verschiedene Methoden und vordefinierte Felder bietet um die Integrität von klassischen komplexen Datenstrukturen wie eine dict oder eine hashmap. 

```python
class PullRequestEvent(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    repository: Repository
    sender: User
```

Das benutzen von klassischen `__init__()` Konstruktoroperationen entfällt, da das vererben von `BaseModel` dies nicht benötigt. Wie man ausserdem sehen kann, befinden sich 2 weitere Modele innerhalb der `PullRequestEvent`-Klasse. Da `PullRequest` und `Repository` beide von `BaseModel` erben, können komplexe verschachtelte Modele __typensicher__ verwendet werden und der Typ eines jeden Feldes ist von anfang an dabei. Beim durchwandern von tiefen `json`-payloads kann dies eine grosse Hilfe sein.

Hier noch ein Beispiel von `PullRequest` und wie darauf zugegriffen werden kann:

```python
class PullRequest(BaseModel):
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: User
    body: Optional[str]
    created_at: str
    updated_at: str
    closed_at: Optional[str]
    merged_at: Optional[str]
    merge_commit_sha: Optional[str]
    assignee: Optional[User]
    assignees: List[User]
    requested_reviewers: List[User]
    requested_teams: List[dict]
    labels: List[Label]
    milestone: Optional[Milestone]
    draft: bool
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    head: Head  
    base: dict
    _links: dict
    author_association: str
    auto_merge: Optional[str]     
    active_lock_reason: Optional[str]

def handlePullRequestEvent(pr: Any) -> None:
    pull_request_event: PullRequestEvent = PullRequestEvent.model_validate(pr)
    print(pull_request_event.pull_request.title)
```

## Patterns

Es werden nicht viele Patterns verwendet, eines werde ich aber für die Abstrahierung des Datenzugriffs verwenden, da es ein sehr einfaches Pattern ist und mit den Prinzipien von REST sogar parallel zueinander sind. Hier ein abgeschnittenes Beispiel zum Repository Pattern zur Verwendung von Basismodelen.

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
...
```

Diese Repository Klasse ist eine [generische Klasse](https://mypy.readthedocs.io/en/stable/generics.html) und erlaubt es mir Typenparameter an die Klasse vor der Instanzierung zu übergeben. Mit den Repository-methoden `list`, `get`, `create`, `update` und `delete`, weiss ich dass ich entweder garantiert ein bestimmtes Basismodel erhalte oder nicht. Als Backend verwende ich dabei Redis und dies dient mir Datenmodelle korrekt in Redis abzulegen und wieder abzuholen.

Die `redis_response_to_pydantic_model()` ist eine rekursive Funktion und validiert die Ausgabe.

### Instanzierung eines Buchrepository

Gehen wir mal davon aus wir möchten Bücher in Redis ablegen und uns sicher sein, dass wir diese im Code wiederverwenden würden. Hier ein python test geschrieben mit [pytest](https://docs.pytest.org/en/stable/) und einem [Redis Testcontainer](https://testcontainers.com). Um zu testen dass unser Repository auch wirklich ein Buch zurückgegeben hat, testen wir das Resultat direkt mit einem Redis Testcontainer

```python
class Book(BaseModel):
    name: str
    pages: int
    author: str

def test_repository_returning_list_of_books():
    rc = redisContainer.get_client(decode_responses=True)
    bookRepo = RedisRepository[Book](rc=rc, key="book")

    result = bookRepo.list()

    assert len(result) == 2 
    assert isinstance(result, List)
    assert isinstance(result[1], Book)
```

Mit diesem Test erstellen wir ein RedisRepository welches die oben genannten Operationen nutzen kann und ein oder mehrere Bücher zurückliefern kann. Dies gilt auch für mutierende Operationen wie `create` oder `update`. Dabei muss ein sogenannter `key` instanziert werden um dem Buch einen key in Redis zu vergeben. Im Hintergrund legt, Redis dann die Werte als **Key-Value-Pair** ab und lässt, dass zurückholen von verschachtelten Objekten zu. Ein Counter wird verwendet, was nichts anderes als ein `integer` in Redis ist, welches bei jeder `create` Operation die Zahl um 1 erhöht.

## Redis

Redis ist eine in-memory Datenbank und baut, anders als relationale Datenbanken, auf simplere Datenstrukturen wie strings, integer oder hashmaps. Damit werden einem Grundsteine hingelegt. Relationen und Verweise, sind für eine solche Datenbank nicht üblich, da Redis vorallem als Cache sich einen Namen gemacht hat. Redis kann anscheinend viel mehr als gedacht und mit der vielseitigkeit und vorallem der Geschwindigkeit dank der starken Nutzung von RAM, stellt Redis einen guten Darsteller für eine minimale Datenbank zur Verfügung. 

Persistenz erreicht Redis durch eine Kombination aus `point-in-time snapshots` und `Append Only File`. Letzteres schreibt jede Schreiboperation von Redis auf ein File in Sequenz und kann so, nach einem Neustart einfach das `Append Only File` auslesen und mit den Snapshots abgleichen. Dies erlaubt Redis immer auf dem Arbeitsspeicher zu arbeiten ohne Einbussen zu machen.

Einige Konzepte in Redis verhalten sich anders und müssen anderst gelöst werden. Wie behalte ich eine Liste von Objekten im Griff, wenn keine incremente automatisch passieren, wie bei einem incrementierenden `PRIMARY KEY` in einer Postgres Datenbank? Wie kann ich sicherstellen, dass auch jede einzelne Operation als Ganzes passiert und keine Inkonsistenzen mit sich bringt? [Indexierung](#Indexierung) und [Pipelines](Pipelines).

### Indexierung 

Bei der Indexierung kann einfach ein neuer `Integer` erstellt werden, welcher im Namen als `counter` asoziiert werden kann. Dieser kann als id verwendet werden und muss vor jeder **write-operation** um 1 erhöht werden. Da der counter nur durch die `create`-methode mit einer [Pipeline](#Pipelines) ausgeführt wird, kann immer ein Wert hinter jedem index von jeglichem Typ entstehen. 

```python
    def create(self, model: BaseModel, options=None) -> bool:
        if options:
            pass

        with self.__rc as rc:
            print("key is", self.__key)
            current_id = f"{self.__key}counter"
                        
            with rc.pipeline() as pipe:
                count = rc.incr(current_id)
                pipe.hset(f"{self.__key}:{count}", mapping=dict(model))
                result = pipe.execute()

            if result[0] == len(model.model_fields.keys()):
                return True

            return False

```

### Pipelines

Mit Pipelines können in Redis sichere Operation sichergestellt werden, sogenannte atomische Operationen. Da Redis keine ähnlichen Abstraktionen anbietet wie andere Datenbanktechnologien wie Primary Keys oder Joins, müssen die Entwickler viele Abstraktionen selber definieren um sichere Datenbankoperationen zu gewährleisten. Wie im obigen Beispiel, wollen wir den Counter ja nur erhöhen, wenn wir tatsächlich die hash-map ablegen können, falls dies nicht passieren sollte, weil die Datenstruktur z.B. Fehler hat, möchten wir dass der Counter wenn möglich wieder zurückgesetzt wird und der Eintrag gar nicht stattfindet. Redis bietet dafür Pipelines an. 

Pipelines ermöglichen dem Entwickler ein Set von Operationen zu definieren, die alle erfolfgreich sein müssen, damit die Änderungen wirksam sein können. Falls nur eine Operation nicht erfolgreich ist, wird ein Rollback gemacht. Redis führt in Wirklichkeit alle Operation gleichzeitig durch um die Latenz zu verringern.

```python
with rc.pipeline() as pipe:
                count = rc.incr(current_id)
                pipe.hset(f"{self.__key}:{count}", mapping=dict(model))
                result = pipe.execute()

```

Mit dieser Codezeile sammeln wir alle Pipeline-Operationen an die alle dasselbe Featureset wie normale Redisoperationen hat da `rc.pipeline()` eine pipe zurückgibt, die von `Redis` erbt. mit `pipe.execute()` führen wir die Operatinen allesamt aus.



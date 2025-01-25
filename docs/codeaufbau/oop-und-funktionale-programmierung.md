---
title: OOP und Funktionale Programmierung
date: 2024-01-19
tags: 
- code 
- python

---

# Einleitung

Angefangen mit Java, Spass mit Ruby, zufrieden mit Go und Typescript und in Konflikt mit Python und trotzdem habe ich einige Konzepte mitgenommen bin froh damit angefangen zu haben. Mit Python konnte ich nie wirklich eine gute Balance zwischen Klassen und Funktionen finden, da sich durch laufende Entwicklung herausgestellt hat, dass ich mit einer event-basierten Architektur besser fahre wie ich es schon mit Javascript mit interaktiven Benutzerevents machen musste. 

Die Umstellung in der Denkweise als vollkommen ojektorientiert zu betrachten ist auch allfällig schwierig vorallem wenn mit Packages gearbeitet wird und die Dependencies steigen. Eine gesunde Mischung ist notwendig um sich den Vorteilen beider Paradigmen anzuwenden. 

Der Unterschied liegt in der Art wie wir das Verhalten des Zustands beinflussen wenn Datenmanipulationen vorgenommen werden. Dies wiederspiegelt sich mit folfenden Unterschidenen in der Denkweise:

- OOP verwaltet Zustände innerhalb von Objekten und legt Wert auf ihre Veränderbarkeit.
- Funktionale Programmierung bevorzugt Unveränderlichkeit und vermeidet Zustandsänderungen.

Man kann sich beides zunutze machen, wenn man sich den Vorteilen und aber auch den Nachteilen bewusst ist. Die Programmiersprache spielt da eine wesentliche Rolle und die Betrachtung der Datenstrukturen beeinflussen die Nutzung und die Umsetzung. 

In Python ist alles ein Objekt, jedoch fehlen Grundkonzepte wie Interfaces zur Verhaltensdeklaration und werden durch zusätzliche eingebauten Packages wie `abc` ergänzt, was gut ist. Jedoch erschwert Python einem die Nutzung der Sprache, da sich Quellen viel auf Features älterer Versionen stützen jedoch eine Empfehlung gemacht wird sich immer wenn möglich auf die neueste Version von Python zu stürzen. Die schnelle Iteration auf syntaktischen Mitteln wie **type hints** und **Generics** fühlen sich nicht ausgereift an, da wahrscheinlich der Fokus auf die Rückwärtskompatibilität und das vereinfachen von APIs abgewendet wurde zugunsten der vielseitigkeit die die Sprache bieten möchte. Python scheint alles zu können, ausser Gut in allem zu sein. 

Folgende Beispiele beschäftigten mich während der Ausführung der Arbeit:

- Dynamische Typen und Type Hints
- Side Effects bei Mutationen
- Builds

Die folgenden Erlebnisse fand ich hingegen gut und weckten mein Interesse in Zukunft eventuell wieder mit Python kleinere Projekte zu schreiben:

- FastAPI
- Ökosystem

## Das Schlechte

### Dynamische Typen und Type Hints

Im Verlauf des Projekts habe ich gemerkt dass ein spezielles Talent erforderlich ist in Python mit Typen zu arbeiten. Die Erfahrung war mager und verursachte bei der Verwendung von externen Packages die ohne Type Hints oder Generics auskommen für Kopfschütteln. Eine effektive Nutzung von redis musste ich zum Beispiel mit Pydantic lösen um effektive Datentypen zu nutzen und generische Aufrufe zu ermöglichen die einem typischerweise entweder das Zielobjekt oder nichts liefern.

Schauen wir uns ein Beispiel von Go an und wie dort die man die statt die Erwartung auf ein Objekt dem Typ einer Klasse erwarten möchte sondern man sich eher auf das Verhalten fokussiert und implizite Vererbung von Verhalten sich auf die einfachheit Auswirken kann:

```go
type Storage[T any] interface {
    Create(item T) error
    Read(id int) (T, error)
    Update(id int, item T) error
    Delete(id int) error
}

type PostgresStorage[T any] struct {
    db *sql.DB
}

func NewPostgresStorage[T any](db *sql.DB) *PostgresStorage[T] {
    return &PostgresStorage[T]{db: db}
}

func (ps *PostgresStorage[T]) Create(item T) error {
    // In a real application, you'd execute a SQL INSERT here.
    // For illustration, we'll just print and pretend it worked.
    fmt.Println("Creating item in Postgres:", item)
    return nil // or return an error if something goes wrong
}

// ...
// Deklaration für Read, Update, Delete

func ProcessStorage[T any](store Storage[T], item T, id int) error {
    // Create a record
    if err := store.Create(item); err != nil {
        return err
    }
}

```

Ja nicht die hübscheste Sprache verglichen zu Python aber wenn man genau hinschaut fallen einem 2 Sachen auf:

- Die Funktion `ProcessStorage(...)` nimmt ein Interface als Parameter an
- Das Interface `Storage` wird gar nicht explizit implementiert

In Go müssen structs die Methoden implizit implementieren um als gültige Implementation eines Interface angesehen zu werden. Da `PostgresStorage` einfach die Methoden deklariert hat die einen Store ausmachen und die gleichen Rückgabewerte zurückgegeben hat, ist es ein gültiger `Store` und kann als Parameter in die öffentliche Funktion `ProcessStorage` übergeben werden.

```go
func main() {
    var db *sql.DB

    storage := NewPostgresStorage[string](db)

    err := ProcessStorage[string](storage, "Example Item", 123)
    if err != nil {
        fmt.Println("Error processing storage:", err)
    }
```
}

### Side Effects bei Mutationen

Was mir aufgefallen ist, ist dass viele Methoden, vorallem Standardmethoden, eher mutierender Natur sind. Dieser Unterschied zu Javascript als dynamische Sprache veränderte wie ich Code schreiben musste enorm. Ich hätte mich sicher besser auf die Dokumentation verlassen können. Nichtsdestotrotz bietete python meistens für solche Fälle keine immutable Alternativen ausser, dass man selber eine Kopie eines Objekts oder eines Arrays erstellen musste um bei `Requests`, keine Transaktionen zu verfälschen. Die Splat Funktionalität gegenüber Python lässt zu wünschen übrig und erschwierigt manchmal das validieren komplexer Objekte bei denen Felder entweder nicht vorhanden sein können oder da sein können und dabei gleichzeitig den type checker glücklich zu machen. Da bietet Typescript eine viel intuitivere Art mit Funktionen welche meistens nicht mutierend auf Datentypen reagieren und einem dabei mit impliziten Typenvererbung eine bessere Arbeit liefert.

Hier ein Beispiel beim umkehren von Listen in Python zu Javascript/Typescript:

**Python:**
```python
my_list = [1, 2, 3]
result = my_list.reverse()

# result == None
# my_list == [3,2,1]
```

In Python ist die Variable `result` leer. Jedoch ist my_list mutiert worden.

**js/ts:**
```js
let arr = [1, 2, 3];
let result = arr.reverse();  
```

in Javascript bleibt arr immernoch gleich und die variable `result` erhält das umgekehrte Array. 

Dabei ist die Alternative in python die `reversed()` methode zu verwenden. Wie komme ich als Konsument deiner Methode darauf zu denken dass sich beide fast gleichbedeutenden methoden unterschiedlich operieren ohne type hints?

Python versucht expressiv zu sein. Doch versteckt sich immer die Frage was verursache ich mit meiner Operation wie kann ich mein Ziel am besten Ausdrücken.

In Javascript kann eine immutable Datenoperation durch das überschreiben der Kopie eines Objektinhalts gleichzeitig mit einer Expression lösen welche sich bei `Put` oder `patch` Operationen als wirksam erweisen.

```js
const originalObject = { foo: 'bar', baz: 42 };
const mergeObject = { foo: 'baz'}

const copyObject = { 
    ...originalObject,
    ...mergeObject
};

// OR

const copyObject = { 
    ...originalObject,
    foo: 'baz'
};

console.log('originalObject:', originalObject); // { foo: 'bar', baz: 42 }
console.log('copyObject:', copyObject);         // { foo: 'baz', baz: 100 }
```

copy Object nimmt den gesamten Inhalt des Objekts (ein dict in python) mit der ... Operation (splat). So erstellen wir eine gemergte shadowCopy des Ursprungsobjekts und können weitermachen. Problem erledigt.

Bei python ist mir meistens nie schlüssig ob es objektorientiert (Verhalten durch Methoden verändern) oder funktional sein möchte (Funktionen definieren das Verhalten von Daten).

### Builds

Ich veröffentliche gerne Releases in Form von Containern. Da ist die Umgebung zur Ausführung von Python masgebend für produktive Docker Builds. Dev Container oder generische python runtime container für testing sind da nicht das Problem. Das Problem von Programmen welche mit Python geschrieben werden sind nur 2:

- Der Python Interpreter
- Die Grösse von produktiven Images und musl libc

Letzteres ist eher ein Problem bei Projekten bei denen die Requirements für Kaltstart und Reiteration strenger sind als im Normalfall, Da auch python images eine  gute Grösse erreichen können. Die Aspekte um Security sind dann eher eine Auswirkung auf die Abhängigkeit einer LAufzeitumgebung und meist vernachläsigbar, müssen aber immer beachtet weden sollte Security priorität haben.

Abgesehen vom Code welcher natürlich sicher geschrieben sein müsste um das PRodukt als sicher ansehen zu können. Zusätzliche Abhängigkeiten verursachen mehr Komponenten mit individuellen CVEs welche gemanaged werden müssen, auch die Wahl des base images bei einem multi stage build in docker um ein minimales produktives image zu nutzen, fällt die Wahl für sichere und minimale docker container meistens auf alpine linux. 

Python besitzt noch manche Bibliotheken und Packages die auf glibc basieren. alpine arbeitet aber mit musl und somit kommen Kompatibilitätsprobleme schon mal vor. Es gibt Wege diese zu lösen, oder auch fertige python-alpine images. Man muss dies einfach in die Containerstrategie aufnehmen, da Abweichungen eher noch geschehen können als gedacht. Ausserdem kommen python oder node images nicht immer gut an da sie meist für Testzwecke in Quantität auf mehreren Hosts getestet werden müssen meist über mehrere Pipelines parallel. Wenn die Versionen bei starker Iteration in Entwicklungsumgebungen eine Rolle spielen und Edge Devices kontinuierlich auf Feature Releases verlassen entstehen 2 Probleme.

- Langsame Kaltstarts
- grosse Images

Dies ist in einer Service-Mesh oder Micro Services Architektur weniger wichtig aber im IOT Bereich mit mobilen Geräten die über begrenzte Bandbreite verfügen doch ein Problem. Vorallem wenn die Verteilung neuer Images in Minutentäkten passieren. 

## Das Gute

### FastAPI

Als Befürworter von minimaleren Webserver-Bibliotheken wie die Standardbibliothek von Go, konnte ich gute Resultate mit FastAPI erzielen um schnell eine einfache und validierte API zu bauen. Dank der Nutzung von Pydantic sind werden automatische HTTP Responses mit guten Fehlerbeschreibungen ausgegeben und eine automatische OpenAPI Spezifikationserstellung aus den Pydantic Schemas ist eine richtig tolle Art die Dokumentation der API immer im Griff zu haben. Dies erspart einem eine Menge Arbeit und war der Hauptgrund wieso ich nicht auf Azure Functions umsteigen wollte, da dort das Feature nur spärlich unterstützt wird.

Andere Features wie authentication, dev-server für testing, asynchrone Operation und eine einfache Nutzung mit Decorators sind eine andere Art Logik in einfache Funktionen zu implementieren. 

Dank des Decorator Patterns werden all diese Funktionen für einen übernommen kann aber in manchen Fällen für zu viel Abstraktion sorgen. Kommt immer darauf an wie viele indiviuelle FastAPI Features man noch verwenden möchte.

### Ökosystem

Das Python Ökosystem ist vielseitig, wenn nicht fast schon zu vielseitig. Wenn man eine potenzielle Bibliothek für ein Problem sucht, hat meistens schon irgendjemand auf pypi eine bibliothek geschrieben oder ein Programm dass deine Probleme lösen könnte. Darunter befinden sich wie bei allen Open-Source Projekten der Haufen der nicht mehr bewirtschaftet wird doch vorallem die 3rd Party Integration von SaaS Produkten oder SDKs gibt es allerhand und werden noch an vielen Orten weitestgehend gut bewirtschaftet. 

Dies sieht man auch an der Verbreitung der Sprache. Man kommt an vielen technischen Gefilden in Kontakt mit Python und kleinere Produkte aber auch riesigie Produkte unserer Zeit sind weitestgehend in Python geschrieben. Dies ist auch zu verdanken dass man Python auf allen möglichen Betriebssystemen meist problemlos installieren kann.

Auch fertige Tools wie Ansible oderdie Azure-Cli welche mit pip installiert werden können und keine Python Kenntnisse benötigen befinden sich in meiner Bibliothek und zeigt wie viele gute Projekte schon mit Python umgesetzt wurden.


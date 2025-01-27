-
title: Testing
date: 2024-01-25
tags:
    - tests
    - bruno
---

# Testing

Tests wurden im [tests Ordner](https://github.com/migueltinembart/ponte/tree/main/tests) geschrieben und sind eine Kombination aus [Pytest](https://docs.pytest.org/en/stable/)-Tests und [Bruno](https://www.usebruno.com)-Tests und können individuell ausgelöst werden. 

## Pytest

[Pytest](https://docs.pytest.org/en/stable/) ist ein Framework zum vereinfachen von Tests und zur Erstellung von einfachen Testumgebungen in Python. pytest ist meiner Meinung nach einfacher als unittest und bietet einige nützliche Features wie initializers, finalizers und mehr um die Voraussetzungen deiner Tests einfacher enkapsulieren zu können. 

### Fixtures vorbereiten

Eine Fixture ist ein Set von Pre Conditions welche erfüllt sein müssen um den Test überhaupt zurchzuführen. Dies ist ein guter Ort um zum Beispiel:

- Eine leere Datenbank mit initialen Daten zu füllen die für das Testing notwendig sind
- Feature Flags zu setzen
- externe APIs auf ihre validität prüfen, falls man davon abhängig ist

> [!INFO]
> In meinem Beispiel wird mit Testcontainers gearbeitet wie in [Tests](/codeaufbau/konzepte.md#instanzierung-eines-buchrepository). Testcontainers sind eine gute Art Dienstabhängigkeiten in den eigenen Tests zu definieren und als Container für die genannten Tests zu nutzen. 

Eine Testcontainer Instanz kann dann in einer Fixture definiert werden und den container und dessen client credentials direkt auslesen.

```python
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


```

Da der Parameter `autouse` auf `True` gesetzt ist, werden die nachfolgenden Tests alle von einer Redis Instanz begleitet und dank des finalizers wieder abgeräumt sobald der letzte Test fertig ist.

## Bruno

Bruno hat eine eigene [DSL](https://www.jetbrains.com/mps/concepts/domain-specific-languages/#:~:text=A%20Domain%20Specific%20Language%20is,from%20the%20field%20or%20domain.) die verwendet werden kann um eine collection abzubilden. Damit können mit der bru cli alle Requests in der Collection angewandt werden. Eine Idee zum Beispiel mit docker compose bru in einem eigenen Container laufen zu lassen um API Requests zu starten um die API zu testen war mal angedacht. Da dies aber nicht Werterbringend in Angesicht der Tatsache des Scopes von Ponte ist, kann dies einfach mal als Idee da stehen.

Momentan nutze ich die Tests lokal um mit eine Webhook Mock Response zu generieren. So kann ich ohne Github den Prozess testen und sehen ob die API die richtigen Validationen durchführt.

# Vorgang

Um die Tests effizient nutzen zu können verwende ich Github Actions um die Tests bei einem Pull Request auszuführen die nach main gepullt werden. Dies erlaubte es mir automatisiert den Stand meiner Abstraktionen zu tracken und für weitere Abstraktionen eine einfache Ausführungsebene zu haben um festzustellen ob eigene Module brechen.

Für eine Github Actions Pipeline muss eine workflow Definition unter `.github/workflows` in deinem git-repository bestehen. Für ponte besteht eine Pipeline unter [.github/workflows/pytest.yaml](https://github.com/migueltinembart/ponte/blob/main/.github/workflows/pytest.yaml) und startet die pytest. Der Workflow startet dann ein Container image für redis anhand des tests und führt diese für verschieden Python Versionen durch.

Man könnte weitere Mechanismen damit verbinden dass die Tests ausschlaggebend dafür wären einen Pull Request erst überhaupt zu mergen oder dass die nächste stage in einer Pipeline erst weiterführen kann. Das inkludieren von Tests macht den Prozess ersichtlich und lässt andere Entscheidungen von den Tests abhängen. Dies führt schlussendlich zu sauberen Code.

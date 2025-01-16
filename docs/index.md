# Ponte

Ponte ist ein ein minimaler Webdienst für die Erstellung von cloud Resourcen anhand eines Konfigurtionsfile im Repository. Das Konfigurationsfile entspricht einem Schema und bietet Autocompletion für die Konfigurationssprache mitHilfe von `json schema`.

## Einführung

Das Ponte entstand aus dem Wunsch heraus, Änderungen an einem Konfigurationsfile in einem Git Repository direkt in den Zielzustand eines Servers überzuführen. 

### Features

Ponte (übersetzt Brücke) reagiert auf Webhooks und reagiert bestimmte Events von Github um folgende Aufgaben anhand eines Beispiels zu übernehmen:

#### Beispiel

1. Ein Pull Request auf den main Branch wir initialisiert. Ein Event wird an Ponte per Pull Request übergeben.
2. Ponte liest vom Branch aus dem Pull Request in einem `ponte.yaml` file die Deklaration für eine Azure VM 
3. Ponte überprüft den Zustand der VM auf Azure anhand des Files
4. Existiert die VM nicht, wird sie erstellt. Ansonsten wird sie zerstört und wiederhergestellt.
5. Auf Github wird eine Nachricht in den Pull Request gesendet, sollte das Deployment abgeschlossen sein und verweiset auf eine url, zur Dateneinsicht.

### Auftrag

Im Auftrag der TBZ erarbeite ich mithilfe der Projektbetreuung von Armin Dörtzback (FaaS) und Philipp Rohr (Projektmanagement). Das Projekt wurde am \<Datum> eingereicht und in die Projektplanung in [Github Projects](https://github.com/users/migueltinembart/projects/5) aufgenommen und in mehrere 2 wöchige Sprints eingeteilt. 

### Motivation

Ich hatte früher viel Spass beim austesten von verschiedenen Programmierkonzepten und Ideen um meine Fähigkeiten als Allrounder zu testen. Meine bescheidenen Fähigkeiten konnte ich bisher nur mit eher kleineren Projekten begnügen und ich wollte ein eigenes kleines aber schlankes Produkt machen und dabei zum 4 mal eine weitere Programmiersprache entdecken. Ich habe Python immer wieder nur aufgehoben und wieder abgesetzt, da Go und Typescript eine gute Kombination für mich war und erhoffe mir eine die erwünschte Geschwindigkeit die Python für den Workflow verspricht.

## Aufbau

// TODO



---
title: Startseite
date: 2024-01-25
tags:
    - ponte
---

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

Folgende Aspekte werden in dieser Arbeit ausführlicher behandelt:

- Aufbau des Codes
    - Konzepte
    - Snippets
    - OOP und Funktionale Programmierung
- Komponenten
    - Abhängigkeiten
    - Entwicklungsworkflow
    - Paketierung und Containerisierung
- Umsetzung und Planung
    - Probleme
    - Lösungen
    - Tests
- Reflexion und Fazit

Die Quellenbeschriebe werden in Form von Markdownlinks so gut wie möglich referenziert und möglichst realitätsgetreu abgebildet.

### Beschreibung zum Aufbau

Um die Aspekte rund um den Code-Aufbau mitsamt konzeptioneller Gedanken und Entscheidungen genauer beschireben zu haben, sind folgende Gliederungen definiert um die grösseren Komponenten der Semesterarbeit einzufangen. 

**Codeaufbaue** ist eine Sammlung von Themen rund um code spezifische Ausdrücke in Ponte. Die Seiten sind eher technisch aufgebaut und beinhalten Design Patterns oder Design Implementationen beschreibt diese ausführlicher.

**Komponenten** legt alle Teile von Ponte zusammen um die Lifecycle-Entscheide und das grundsätzliche Design besser zu beschreiben und diese auszulegen. Themen wie das Vorgehen bei Updates in Libraries wird zum Beispiel dort angeschnitten.
**Umsetzung** behandelt die Ausführung und Planung von Ponte und wo es Probleme gab oder wo diese gelöst wurden. Die nötigen Tools und wie sie bei der Ausgührung beigetragen haben haben dort ihren Platz.

#### Codeaufbau

- [Konzepte](/codeaufbau/konzepte.md): Beschreibt Abstraktionen und die Nutzung verschiedener Techniken und vergleicht diese mit anderen Programmierparadigmen.
- [OOP und Funktionale Programmierung](/codeaufbau/oop-und-funktionale-programmierung.md): Ist eine Sammlung von Gedanken rund um 
- [Snippets](/codeaufbau/snippets.md): Sind eine Sammlung von nützlichen eher generische Lösungen und Beispiele

#### Komponenten

- [Abhängigkeiten](/komponenten/abhaengigkeiten.md): Beschreibt die Abhängigkeiten und sammelt diese in Unterkapitel. Wie muss vorgegangen werden wenn z.B. eine neue Breaking change in einer Library auftaucht.
- [Entwicklungsworkflow](/komponenten/entwicklungsworkflow.md): Zeigt Entwicklungskomponenten und wie diese für die mögliche Kollaboration mit mehreren Entwicklern genutzt werden kann.
- [Paketierung und Containerierisierung](/komponenten/paketierung-und-containerisierung.md): Zeigt auf was geachtet werden muss wenn die Software als Container Image zur Verfügung stellen muss. Wie werden Vulnerabilities assessed.

#### Umstzung

- [Nutzung](/umsetzung/nutzung.md): Zeigt wie man Ponte mit Docker verwendet und die Variabeln nötig um ponte richtig einzusetzen
- [Testing](/umsetzung/testing.md): Erklärt wie bei Tests vorgegangen wurde um die Funktion von eigenen Abstraktionen als Unit Tests zu testen
- [Tools](/umsetzung/Tools): Zeigt wie mit den verschieden Tools umgeganen wurde und listet die genutzten Resourcen die für die Umsetzung des Projekts nötig waren.


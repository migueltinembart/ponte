---
title: Continuous Integration
date: 2024-01-25
tags:
    - ci 
    - tests
    - github-actions
---

# Continuous Integration

Continuous Integration beschreibt den Prozess den Code immer wieder integrierbar zu machen und durch eine Automation den Bau Prozess der Software nach bestimmten Kriterien wiederaufzunehmen. Dabei ensteht ein Artefakt und dieses Artefakt kann dann in eine Release aufgenommen. Ein Artefakt kann alles sein, ein tarball, ein Dockerfile oder eine npm-package und je nach Artifact Registry sieht die Kompatibilität anders aus.

Ponte hinterlässt nach jedem Tag ein Container Image welches von der Github Container Registry zur Verfügung gestellt wird. Dieses Image kann von jeder Container Runtime ausgeführt und gepullt werden sofern man danach wünscht. Den Prozess zur automatischen Erstellung von Container Image Releases wird hier gründlich beschrieben.

## Aufbau

Folgende Kriterien müssen erfüllt sein:

- ein funktionierendes Dockerfile mit dem Build deiner Applikation
- Github 
- Github Actions 

### Dockerfile 

Das Dockerfile ist eher simpel. Python Applikationen haben keinen grossen Nutzen davon mit multistage-builds zu funktionieren, da das Image dadurch nicht wirklich viel an Masse verliert. Die Python Laufzeitumgebung ist an sich wenige hundert MB gross und wenn man die Schichten nicht zu hoch treibt, können die Images auch klein genug so geschrieben werden:

```Dockerfile
FROM python:3.12-slim


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

Als Image wird eine slim Version des Python Images genommen, welches auf Debian basiert. Debian images bieten wenn möglich auch slim Varianten an welche weniger base Packages anbieten um die Grösse zu reduzieren. 

Am Ende wird der Startbefehl als Array von Argumenten übergeben und das Image kann mit folgendem Befehl dann gebaut werden:

```bash
docker build -t ghcr.io/<owner>/<repo>:<version> .
```

### Github Actions

Github Actions bietet eine CI/CD Plattform mit einer soliden free tier welche verwendet werden kann um arbiträre jobs für dein Repository auszuführen. Von der Dokumentationswebsite für die Semesterarbeit bis hin zu den Tests sind mehrere Github Actions Workflows involviert. Ihre modulare Art mit Actions aus der Community gibt Entwicklern die Möglichkeit relativ schnell einfache aber effiziente Pipelines zu schreiben um argwöhnische Tasks der Automation zu überlassen.

Eine Workflow Definition schreibt sich innerhalb des Ordners `.github/workflows` in einem `.yaml`-file. Für einfaches Autocomplete kann gerne die Extension für Github Actions installiert werden um das json schema einfach zu laden.

Eine Workflow Definition kann so aussehen:

```yaml
name: Unit Tests
on: 
  pull_request

jobs:
    build:
        runs-on: ubuntu-latest
        strategy:
            matrix:
                python-version: ["3.12", "3.13"]
        steps:
            - uses: actions/checkout@v4
            - name: Setup python ${{ matrix.python-version }}
              uses: actions/setup-python@v5
              with:
                python-version: ${{  matrix.python-version }}
            - name: install requirements.txt
              run: pip install -r requirements.txt

            - name: run unit tests
              run: coverage run -m pytest -v -s
            - name: Generate Coverage Report  
              run: |  
                coverage report -m
```

Dabei fallen folgende Punkte auf:

- Die Pipeline wird durch eine Matrix Funktion auf mehreren Instanzen von Python ausgeführt
- pytest wird einer coverage ausgeführt

Diese Pipeline bietet mir die Möglichkeit nach der Ausführung einen Coverage Report zu erhalten.

![Bild von Coverage Report](/assets/gh_actions_test_coverage_report.png)

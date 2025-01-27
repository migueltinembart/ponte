---
title: Entwicklungsworkflow
date: 2025-01-22
tags:
    - components
    - deps
    - illustration
---

# Entwicklungsworkflow

Unter einem Entwicklungsworkflow redet man von einem Weg wie man die richtigen Tools bereitstellt und diese einsetzt um einen produktiven Workflow zu entwickeln und mehr Zeit für die Arbeit investieren kann die nötig ist um als Team zu kollaborieren. 

Folgende Features und Tools helfen mir aber auch meinem Team mit der Erstellung von einheitlichen Umgebung und die Premise die Qualität der Arbeit aufrecht zu erhalten.

- Devcontainers
- Testcontainers
- Hot-Module reload
- pre-commit

Mit diesen 4 Tools können manche Aspekte in der Zusammenarbeit und der Bootstraping Phase eines Projekts helfen und bieten ein alternatives Package um das Onboarding zu vereinfachen.

## Devcontainers

Eine Open Source Contribution von Microsoft und ein fantastischer Weg fertige Entwicklungsumgebungen für Teams bereitszustellen. Mit Devcontainern können mobile Arbeitsumgebungen geschaffen werden, welche im Repository eingecheckt werden können und von jedem Beteiligten am Repository als Devcontainer gestartet wird. Die Integration mit VSCode ist gelungen und beim starten eines Devcontainers geht VSCode direkt in den Container hinein. Der Container installiert alle nötigen definierten Abhängigkeiten wie Programme, VSCode Extensions, bindet mounts in den Container und dein Code ist nun in einem Container. 

Ein Devcontainer kann von einem klassischen Container Image aber auch mit einem Dockerfile oder einem Dockercompose File benutzt werden. Docker Compose ist demnach interessant, da deine Abhängigkeiten neben deinem Devcontainer mitinstalliert werden können und du praktisch deinen Code neben deinem Workload wie deiner Postgresql Datenbank ausführen kannst.

Ausserdem sind alle vom Team definierten Tools so in einem Dockerfile oder im `devcontainer.json` und die Umgebung auf die Firma angepasst werden. 

Wenn du es richtig machst kannst du sogar dein production image als devcontainer verwenden und die Tools darüberziehen um eine nähe mit deiner Umgebung zu haben die vorerst nicht möglich war.

## Testcontainers

Bei Testcontainers ist es anders als bei Devcontainers. Testscontainers ist eine Bibliothek oder je nach Betrachtungswinkel ein Package welches für viele verschiedene Programmiersprachen vorhanden ist. Darunter gehören Python, Typescript, Go und etliche weitere dazu. Testcontainers erlaubt es dir in deinem Code für deine Tests, container mit deinen Abhängigkeiten zu definieren. Als Beispiel wenn man einen richtigen E2E-Integrationstest schreiben möchte und dabei dies auf einer Datenbank testen müsste, müsste die Datenbank jedes mal mit etwas ähnlichem wie `DROP TABLE ...` bereinigt werden um für den nächsten Test eine gewisse Konsistenz aufzubauen.

Mit Testcontainern kann beim ausführen deines Tests ein Container mit deiner Datenbank hochgefahren werden und deine Tests direkt darin ausführen. Nachdem die Tests durch sind, wird der Container wieder heruntergefahren und da kein storage mitgegeben wurde für die persistenz auch keine Daten mehr auf der Datenbank.

Testcontainers erlauben es uns Tests mobil zu halten und machen unsere CI Integrationen einfacher, da alle notwendigkeiten direkt in den Tests definiert sind und nur Docker als Dependency notwendig ist.

## Hot-Module Reload

Ein Feature welches vorallem mit Dev Servern in etlichen anderen Programmiersprachen und Frameworks verwendet wird ist ein Live Server bzw. die Möglichkeit deinen Entwicklungsserver während dem entwickeln neustarten zu können um die neuen Änderungen direkt testen zu können.

Bei einem Webserver ist das in der Regel nicht schlimm, da dies durch Test Frameworks wie Bruno abgelöst werden kann, aber bei Frontend Projekten mit Javascript kann ein Hot-Module Reload fähiger Server viel Zeit in der Entwicklung sparen. 

## pre-commit

Pre-commit ist ein mit Python entwickeltes Tool dass darauf abzielt pre-commit hooks programmiersprachenunabhängig zu schreiben und als hooks über Repositories als Module anzubieten. Die Community hat etliche Repositories mit nützlichen Hooks.

Pre-commit kann gut in Devcontainer eingebunden werden als Tool um die Konsistenz von Commits besser aufrecht zu erhalten. 

Ein Beispiel mit Terraform:

Wir wollen fehlgeschlagene Pipelines wegen vergessenen `terraform validate` Instruktionen welche wenige Sekunden auf den lokalen Rechnern kosten würde. Eine fehlgeschlagene Pipeline kostet wieder Zeit, da ein Pull Request eröffnet werden muss, diese nochmals durch ein peer-review durch muss und dann gemergt wird um durch die Pipeline wieder aufgehoben zu werden. Hätte man ein `terraform validate` vorher ausgeführt hätte man den Fehler frühzeitig entdeckt und man hätte mit einem commit die Änderungen durch die Validierungsphase durchbringen können. 

Mit Pre-commit wird vor dem commit einfach `pre-commit` ausgeführt. Anhand eines `pre-commit.yaml` werden die verschiedenen Hooks ausgelesen, eingerichtet und ausgeführt. Bei Terraform könnte das zum Beispiel:

- terraform validate (terraform validieren)
- terraform fmt (Formattierung vereinheitlichen)
- terraform docs (Eine Dokumentation des Moduls erstellen lassen)

So bleibt die Dokumentation immer au dem neuesten Stand, der Code ist immer richtig formattiert und validiert bevor ein commit ausgeführt werden kann. Sollte eines der Operationen fehlschlagen wird pre-commit einer error code von 1 ausgeben und der pre-commit ist fehlgeschlagen.



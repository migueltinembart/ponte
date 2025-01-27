---
title: Reflextion und Fazit
date: 2024-01-25
---

# Reflexion 

## Zeitplanung

Durch das jonglieren von Familie, Arbeit und Schule muss ich einbussen in der Zeit meistens am Abend machen. Da ich zukünftig meine Angelegenheiten besser managen möchte, möchte ich zukünftig einen verbesserten Zeitplan für Projekte und Familie, aber sogar wieder Zeit für Hobbies wie das Homelabben zurückgewinnen. Es gab zu viele Zeitlücken an denen ich nicht am Prjekt arbeiten konnte und somit den Faden verloren habe. Dies erhöhte meine Zeit um die alten Codestücke die ich zusammengelegt habe richtig zu identifizieren. Code zu schreiben ist eine Sache der Konsistenz und zeigt am besten Resultate wenn man Konsequent Fehler macht und mitdiesen Fehlern neue Wege findet die Probleme zu lösen bei denen man früher scheiterte.

Die Zeit an denen wir nicht an der nächsten Semesterarbeit arbeiten, kommt gut gelegen um solche Angelegenheiten anzupacken und mit einer neuen Strategie am nächsten Projekt zu arbeiten. Falls sich die Schule es sich nochmals überdenken würde Projektarbeiten zu zweit zu machen, würde ich dies sogar gerne als Option annehmen, da ich mich vorallem um verschieden gruppierte Gruppen am meisten meine Stärken ausüben kann.

## Devcontainer für Kollaboration 

Bei der Nutzung von Entwicklertools könnten einige Änderungen vorgenommen werden. Zum einen werden Tests auf Github mit über Testcontainer gemacht. Jedoch könnte potenziell mit einem Devcontainer die Tests über einen pre-commit gemacht werden. So könnte man potenziell einfache formattierungen, linting und einfache unit-tests zur stabilität vom Produkt beitragen.

Beim Devcontainer sollte möglichst minimal fortgegangen werden um ein möglichst einfaches Onboarding möglich zu machen. zukünftig werde ich nur noch minimale Extensions mitgeben aber den pip install vorgang nicht mehr beim starten des Containers übernehmen. Ein Enwickler der Python nutzt, sollte wissen wie eine virtual environment genutzt werden muss und die Abhängigkeiten mit `pip install -r requirements.txt` zu installieren.

## Logging

Ich hätte Logging von Anfang an mit in das Design der Applikation mitnehmen müssen. Das nachträgliche setzen von richtigen Log Messages mit dem richtigen Loglevel ist eine Arbeit für sich und müsste mit einer Story erweitert werden um eine richtige Logging Struktur aufzubauen und mitunter könnte wiederum das Exception Handling damit aufgeräumt werden. Dies werde ich bei der nächsten Applikation mitnehmen und mit ins Konzept planen.

# Fazit

Einige scharfe Kanten gäbe es noch auszubügeln und Features könnten noch eingebaut werden. Das sind alles aber Sachen die kann man kontinuierlich am Produkt verbessern und auf die Reaktion der Nutzer hoffen um die Applikation in Zukunft besser gestalten zu können. Im grossen und Ganzen konnte ich wieder vieles für das nächste Projekt mitnehmen und habe neue Use Cases für Python gefunden, bei denen ich früher eher davon abgeraten hätte. Meine initialen negativen Vorhersagen zu Python haben sich nicht immer bewarheitet und die Aufnahme von Requirements und das Auslegen von Abhängigkeiten für die Planung zukünftiger Änderungen und die Auswirkungen auszulegen hat mir eine neue Perspektive zur Betreibung einer Softwarelösung gezeigt. 

Ein eventgetriebenes Design brachte Challenges mit sich doch machte es Spass mich an einer neuen Challenge auszuprobieen. Dies brachte mich der Sprache Python näher und zeigte mir den Umgang damit besser einzuschätzen.

Ein grosses Problem während meiner Entwicklung war das auslegen der verschiedenen Files zur Einteilung von Packages da ich aus anderen Programmiersprachen mir anderes gewohnt war, diese Konvention zu durchbrechen kostete mich starkes ermahnen aber schlussendlich konnte ich trotzdem eine geeignete Lösung finden mit der ich mich zufrieden geben konnte und meine Entwicklung weniger stark ausbremsen.

Für die Zukunft nehme ich mir die nötige Konsistenz zu Herzen die nötig ist um beim nächsten Softwareprojekt mehr Zeit und Energie in die Planung und das Aufteilen von unabhängigen, kleinen aber effektiven Aufgaben die sich näher an den Nutzen als an nette Abstraktionen lehnt.



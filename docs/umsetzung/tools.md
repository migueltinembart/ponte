---
title: Tools
date: 2024-01-25
---

# Tools

Ponte wurde mithilfe von verschiedenen Tools erstellt. Abgesehen von der Programmiersprache und deren Bibliotheken, sind auch andere Tools für die Entstehung des Tools mitverantwortlich. Dazu zählen externe Tools wie SaaS Produkte, Cli Tools oder einfache Applikationen oder Formate.

Folgende Tools und Features werden behandelt:

- Terminal und tmux
- Neovim und dutzende Extensions
- Github
- Devcontainer Cli
- Bruno und Brulang

## Terminal und Tmux

Seit anfang 2024 ist das Terminal meine neue Arbeitsumgebung ob privat oder bei meinem Arbeitgeber. Die wichtigsten Tools haben sich in den letzten Jahren vom klassischen Desktop auf DevOps orientierte Tools in der Cli verschoben und bieten den Vorteil dass sie einfach auszuführen und meist auch zu installieren sind. Bei Linux gibt es allerhand Package Manager und Mac os hat homebrew um externe Packages einfach mit 3 Wörtern zu installieren. Um mehrere Tasks einfach zu managen bietet sich tmux an und erweitert die Shell um Fenster und Tiles um mehrere Sessions bereitzustellen und mit wenigen Tastaturkombinationen hat man einen geeigneten Window-Manager innerhalb des Terminals.

Ein paar Cli Tools die ich täglich bei der Arbeit nutze:

- lazygit
- neovim
- terraform
- kubectl
- jq

## Neovim
d
Neovim ist eine erweiterte Version von Vim, welches eine Erweiterung von vi ist. Neovim hat ein Merkmal dass sich von seinen älteren Iterationen abhebt und dass ist die Erweiterbarkeit mittels lua. Eine leicht zu lernende Programmiersprache welche mit Tables verwendet und sehr funktional aufgebaut ist. Dutzende Plugin sind auf Github erhältich und verwandeln Neovim in einen vollständigen Code Editor mit Syntax Highlighting und Autocompletion. Das andere Merkmal von Neovim sind die Tastenkombinationen und dessen erweiterbarkeit und ermöglichen so, wenn gemeistert, für einen schnelleren Workflow als wenn man mit einem konventionellen Desktop Editor arbeitet. Ponte wurde zu 100% mit Neovim geschrieben um meine Erfahrungen mit Neovim zu verbessern und neue Keybindings zu lernen welche mir persönlich zugeschnitten sind.

## Github

Ich verwende Github schon lange und habe viele Arbeiten darin geschrieben, die meisten jedoch waren nur kleinere Snippets von Demo-Applikationen. Viele davon archiviert, jedoch bewundere ich die vielen Features die Github anbietet und die Wege wie man aus einem Repo eine komplete Applikation mit CI und CD entwickeln kann ist ein Merkmal, dass mich dazu führen wird zukünftig den AZ-400 zusätzlich zu meinem AZ-104 zu machen. Die Bereiche von Devops und Gitops interessieren mich enorm und ich erhoffe mir zukünftig mehr aus Github als Service zu machen, zumal ihre API grosszügigerweise gratis ist und enorm viel den Entwicklern überlässt. 

Seit meinem ersten Modulen für das AZ-400 bei denen Github dabei waren, war ich verblüfft was ich noch alles nicht über git und vorallem Github kannte und bieten für kleine Entwickler und Engineers eine geeignete Plattform und schelle Sandbox-Projekte bereitzustellen.

### Github Actions

Mit Github Actions wird zum einen die Dokumentation bereitgestellt, aber auch das Docker image welches zur Verfügung steht. Github Actions ist vorallem durch die Community erstellten Actions enorm mächtig und modularisiert deine Pipelines für die bessere Wiederverwendung Actions. Gegenüber von Jenkins ist Github Actions relativ einfach zu lernen und vorallem weniger Fehleranfällig da die meisten Plugins eher zielgerichtet sind und einfachere Anpassungen mittels Umgebungsvariabeln und einer simplen und abgespeckten DAG Engine (Direct Acyclic Graph) können weniger Fehler durch die Ausführung der Pipeline selbst entstehen. Die flexibilität und die integrierte Plattform mit ihrer eigenen API für Issues, PRs oder Releases sind starke Gamechanger.

## Devcontainer Cli

Microsoft bietet grosszügigerweise auch für Devcontainer eine Cli an. Das Open Source Projekt ist minimaler als das Setup welches mit VSCode möglich ist, aber die Entwickler scheinen daran interessiert mehr Features in Zukunft anzubieten. Fürs erste reicht es vollkommen aus einer Devcontainer Definition zu starten und darin Neovim und dotfiles als Feature anzulegen um meine Neovim Konfiguration im Devcontainer zu replizieren. So kann ich mein Neovim Setup auch zur Arbeit nehmen.

## Bruno

Bruno ist ein Open Source Ersatz für Postman. Dies kommt gelegen, da mir die letzten Änderungen ihrer Geschäftsbedingungen nicht gefallen haben, trotz dass Postman an sich ein wirklich tolles Produkt ist. Jedoch entstehen durch das Erzwingen eines Kundenkontos für die Nutzung des Clients und die erzwungene Anmeldung Fragezeichen wenn es um die Privatsphäre und vorallem um die APIs und Secrets welche mit Postman behandelt werden könnten. Dieses Gefühl wird verstärkt wenn man sieht dass es sich Postman um eine Web Applikation handelt, die mittels eine Engine für den Browser befähigt zum laufen befähigt wurde einem eigenen Renderer. 

Dieses Ereigniss stellte mich auf die Suche nach Alernativen und ich sah Bruno. Bruno ist sozusagen eine nahe Kopie von Postman und bietet zusätzlich auch noch eine Cli mitsamt einer eigenen deklarativen Sprache um Collections zu definieren. Brulang nennt sich die Sprache und kann von bru verwendet werden um e2e tests auf ponte anzuwenden. Das verpacken von bru in einen Container könnte sich als nützlich ergeben in der Zukunft.


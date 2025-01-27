---
title: Nutzung
date: 2024-01-25
---

# Nutzung

Die Nutzung von Ponte sollte wenn es als modul installiert wird, sich wie jede andere Applikation verhalten. Momentan ist dieses Feature jedoch noch nicht implementiert, da noch einige puzzleteile für eine richtige cli Applikation fehlen.Die Nutzung würde sich dann bei richtiger Implementierung in etwa so anfühlen. 

```bash
ponte --gh-app-id <app-id> \
      --microsoft-client-id <client-id> \
      --microsoft-tenant-id <tenant-id> \
      --microsoft-client-secret <client-secret>
```

## Mit Docker

Die momentane Nutzung von Ponte schliesst sich ausschliesslich auf den Webserver und den zu starten. Dieser erwartet ebenfalls identisch und kann auch die variabeln als Umgebungsvariabeln einlesen. 

```bash
docker run --rm ghcr.io/migueltinembart/ponte \ 
    --gh-app-id <app-id> \
    --client-id <client-id> \
    --tenant-id <tenant-id> \
    --client-secret <client-secret>
```

Dabei werden die Argumente dem Container direkt übergeben. Ausserdem unterstützt der Container das übergeben der Identitätsinformationen mit einer managed identity dank Azure SDK Integration. Potenziell wäre es also möglich auf Azure VMs oder in Container Apps die managed identity zu übernehmen und sich damit direkt als diese Auszugeben. Somit wären nur noch die Github Daten zu übergeben und es entfallen credentialübergaben, was die Sicherheit der Ausführung erhöht.

## Mit Umgebungsvariabeln

Als Alternative die Version mit Umgebungsvariabeln:

```bash
docker run --rm \
  -e GH_APP_ID=<app-id> \
  -e MICROSOFT_CLIENT_ID=<client-id> \
  -e MICROSOFT_TENANT_ID=<tenant-id> \
  -e MICROSOFT_CLIENT_SECRET=<client-secret> \
  ghcr-io/migueltinembart/ponte
```

## Maintenance

Logs werden wie üblich direkt in die Konsole geloggt. Es wurde so viel wie möglich mit Loguri gearbeitet um auch während der Laufphase des Applikation einzusehen. Der Loglevel kann konventionell über die Umgebungsvariable `LOG_LEVEL` angepasst werden. Momentan sind nicht alle Log Levels vollkommen eingefangen und Debug bietet momentan minimale Messages. Dies könnte in der Nachzeit angepasst werden.

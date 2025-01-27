---
title: Nutzung
date: 2024-01-25
---

# Nutzung

Unter dem [Repository von Ponte](https://github.com/migueltinembart/ponte) ist das `README` der Seite zu sehen an der die Nutzung auch nochmals in Kürze beschrieben wird. 

Die Nutzung von Ponte sollte wenn es als modul installiert wird, sich wie jede andere Applikation verhalten. Momentan ist dieses Feature jedoch noch nicht implementiert, da noch einige puzzleteile für eine richtige cli Applikation fehlen.Die Nutzung würde sich dann bei richtiger Implementierung in etwa so anfühlen. 

```bash
ponte --gh-app-id <app-id> \
      --azure-client-id <client-id> \
      --azure-tenant-id <tenant-id> \
      --azure-client-secret <client-secret>
```

## Mit Docker

Die momentane Nutzung von Ponte schliesst sich ausschliesslich auf den Webserver und den zu starten. Dieser erwartet ebenfalls identisch und kann auch die variabeln als Umgebungsvariabeln einlesen. 

```bash
docker run --rm ghcr.io/migueltinembart/ponte \ 
    --gh-app-id <app-id> \
    --azure-client-id <client-id> \
    --azure-tenant-id <tenant-id> \
    --azure-client-secret <client-secret>
```

Dabei werden die Argumente dem Container direkt übergeben. Ausserdem unterstützt der Container das übergeben der Identitätsinformationen mit einer managed identity dank Azure SDK Integration. Potenziell wäre es also möglich auf Azure VMs oder in Container Apps die managed identity zu übernehmen und sich damit direkt als diese Auszugeben. Somit wären nur noch die Github Daten zu übergeben und es entfallen credentialübergaben, was die Sicherheit der Ausführung erhöht.

## Mit Umgebungsvariabeln

Als Alternative die Version mit Umgebungsvariabeln:

```bash
docker run --rm \
  -e GH_APP_ID=<app-id> \
  -e GH_CLIENT_SECRET=<app-id> \
  -e AZURE_CLIENT_ID=<client-id> \
  -e AZURE_TENANT_ID=<tenant-id> \
  -e AZURE_CLIENT_SECRET=<client-secret> \
  ghcr-io/migueltinembart/ponte
```

Eine Auflistung aller übergebbaren Umgebungsvariabeln sind unten abgebildet:

| Variable name       | Value |
| --- | --- |
| AZURE_CLIENT_ID     |	ID of a Microsoft Entra application |
| AZURE_TENANT_ID     |	ID of the application's Microsoft Entra tenant | 
| AZURE_CLIENT_SECRET |	one of the application's client secrets | 
| REDIS_DSN | Supply the connectionstring to your redis instance |
| GH_APP_ID           | The Application ID of your Github App |
| GH_CLIENT_SECRET | The Client secret of you gh app |
| GH_WEBHOOK_SECRET | (optional) supply a webhook secret |
| BASE_URL | (optional) Supply the base url for the app |



## Maintenance

Logs werden wie üblich direkt in die Konsole geloggt. Es wurde so viel wie möglich mit Loguri gearbeitet um auch während der Laufphase des Applikation einzusehen. Der Loglevel kann konventionell über die Umgebungsvariable `LOG_LEVEL` angepasst werden. Momentan sind nicht alle Log Levels vollkommen eingefangen und Debug bietet momentan minimale Messages. Dies könnte in der Nachzeit angepasst werden.

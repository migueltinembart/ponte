# Ponte

Ponte is a containerized Python application designed to act as a lightweight “bridge” between a Git repository and the target state of a server. It listens for specific events (e.g., code pushes or PR merges) and triggers additional automations accordingly. Ponte can be configured using either CLI arguments or environment variables, making it flexible to run in various environments—local, cloud, or on-prem.

## Features

- Event-Driven: Automatically triggers workflows or updates upon Git events.
- Lightweight: Minimal overhead and easy to deploy as a container.
- Configurable: Set parameters via CLI flags or environment variables.
- Extendable: Integrate with other services or APIs for advanced automation.

## Usage

Running via CLI Arguments

```
ponte --gh-app-id <app-id> \
      --client-id <client-id> \
      --tenant-id <tenant-id> \
      --client-secret <client-secret>
```

This starts Ponte with all necessary parameters passed directly to the command.

### Running in a Docker Container

You can also run `ponte` as a docker container if you want

```
docker run --rm \
  -e GH_APP_ID=<app-id> \
  -e AZURE_CLIENT_ID=<client-id> \
  -e AZURE_TENANT_ID=<tenant-id> \
  -e AZURE_CLIENT_SECRET=<client-secret> \
  my-registry/ponte:latest
```

## Configuration

Ponte accepts the following parameters either as environment variables. If both are provided, CLI arguments take precedence.

Service principal with secret

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

## Contributing

Fork this repository and clone it locally.
Create a new feature branch for your changes.
Commit your changes and push them to your GitHub fork.
Create a Pull Request to have your changes reviewed and merged.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


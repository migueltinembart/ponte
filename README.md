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
  ghcr.io/migueltinembart/ponte \
  --gh-app-id <app-id> \
  --client-id <client-id> \
  --tenant-id <tenant-id> \
  --client-secret <client-secret>
```

Alternatively, you can provide the same configuration through environment variables:

```
docker run --rm \
  -e GH_APP_ID=<app-id> \
  -e CLIENT_ID=<client-id> \
  -e TENANT_ID=<tenant-id> \
  -e CLIENT_SECRET=<client-secret> \
  my-registry/ponte:latest
```

## Configuration

Ponte accepts the following parameters either as CLI arguments or environment variables. If both are provided, CLI arguments take precedence.

Environment Variable	CLI Flag	Description
GH_APP_ID	--gh-app-id	The GitHub App ID used for authentication and event processing.
CLIENT_ID	--client-id	The client_id (application_id) to an entra id app registrastration.
TENANT_ID	--tenant-id	The tenant_id of your entra id tenant.
CLIENT_SECRET	--client-secret	The client secret.

## Contributing

Fork this repository and clone it locally.
Create a new feature branch for your changes.
Commit your changes and push them to your GitHub fork.
Create a Pull Request to have your changes reviewed and merged.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


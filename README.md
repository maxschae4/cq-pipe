# cq-pipe

A python example project demonstrating a deduplication pipeline utilizing celery, pydantic, and mongodb

## Development

### Prerequisites

While I attempt to provide all the tooling within a container, this requires a baseline installation and configuration of podman and distrobox.
See [the toolbox README](./toolbox/README.md) for additional instructions.

### Entry

From the `toolbox` directory, run `make toolbox` and `make enter` on the host to create/enter a development environment.

n.b. This will create a directory and file on your host for seemless integration with VSCode (my preferred editor) at:
`${HOME}/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/imageConfigs`

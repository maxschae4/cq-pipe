# toolbox

toolbox leverages [distrobox](https://distrobox.it/) to provide all the tools necessary for using this repository in a declarative way in an Ubuntu environment.
The host doesn't need to be Ubuntu.

## Intention and Explanation

Teams need a common set of tools (especially their versions!) to ensure critical operations are repeatable and avoid troubleshooting tools during emergencies.
Defining these in a container enables declarative iteration.
We provide a developer with their familiar home environment (PS1) etc, while ensuring that the tools they're using match expectations.
This also drastically simplifies onboarding new developers since all the tools (with the correct versions) are provided.

## Prerequisites

### Podman

Install and configure [podman](https://podman.io/docs/installation#linux-distributions).
Ideally, configure [rootless mode](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md).

### Distrobox

Install [distrobox](https://distrobox.it/).

```sh
# we'll install it to your ~/.local directory (you do have ~/.local/bin in your $PATH, right?)
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --prefix ~/.local
```

## Build and Create the toolbox container(s)

Build the base container image from the file.
The **base** container holds the fundamental tools required by the project and a set of developer convenience tools.

```sh
# move to the toolbox directory
cd toolbox
# create a toolbox from the base image
make toolbox
```

## Usage

Enter the toolbox container

```sh
make enter
```

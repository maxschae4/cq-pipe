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

## Tasks

After digging in and building a couple Makefiles, I was reminded of a few things:

- We're (ab)using `make` just because it's available "by default"
- I dislike `make` generally (syntax, learning-curve, etc)
- Maintaining `make` and separate documentation is a chore

In a past job, we had:

- `make`
- shell scripts
- python scripts
- jupyter notebooks
- golang command-line tools
- npm scripts
- and more

Each of these came with separate documentation.

Beyond that, we maintained another `docs/` directory which itself included Markdown with yet more commands.
Many of these we'd end up copy-pasting into a terminal, munging, and hoping for the best.
Most of this was constantly out of date.

And then I realized `make` wasn't included in the toolbox container.
Thus began a search for a better tool:

I stumbled upon [xc](https://github.com/joerdav/xc) in [awesome-go](https://github.com/avelino/awesome-go).

By making the documentation executable, we can ensure that the entrypoints to our code are approachable and kept current at the same time.

### lint

Provides a top-level `lint` target using the [super-linter](https://github.com/super-linter/super-linter) project.
It works by spawning a separate container on the host.

Give it a try from inside the toolbox container with `xc lint`.

```sh
export GIT_DIR=$(git rev-parse --show-toplevel)
flatpak-spawn --host podman run --rm \
    --env RUN_LOCAL=true --env USE_FIND_ALGORITHM=true \
    --volume "${GIT_DIR}":/tmp/lint \
    ghcr.io/super-linter/super-linter:slim-latest
```

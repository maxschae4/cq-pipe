# cq-pipe

A python example project demonstrating a deduplication pipeline utilizing celery, pydantic, and mongodb.

I've gone fairly deep in this project to explore a few ideas I've had kicking around.
Mostly involving trying to improve the development workflow in a complex environment.

I've been running celery in production for years, so taking that approach was a natural fit.
Batch processing definitely might not be the right approach once we hit millions of records.
And I'd bet that before-hand, we'd need to instrument API rate-limit handling among many other things.
I've also dropped the vast majority of the source data from the provided APIs to focus on the core principal of deduplication.

As a sidenote, I've obscured what might be a real Apple Serial number in the data.
Apple indicates these are considered sensitive information.

![image of deduplicated hosts from mongo express](/deduplicated_hosts.png?raw=true "Optional Title")

## Quickstart

### Prerequisites

docker/podman or configured and running rabbitmq/mongodb services

### Without going deep into the development workflow


```sh
# start all services, celery may complain until rabbitmq is up
pip install --user poetry
poetry install
cp .env.sample .env
```

**configure your `.env` file!**

```sh
podman-compose up --detach
# source environment variable file
set -o allexport
source .env
set +o allexport
# run the celery worker if you're not using the docker-composed services
poetry run celery --app "cq_pipe" worker --loglevel INFO
poetry run python3
```

start the extraction manually

```py
from cq_pipe.tasks import extract_crowdstrike_hosts, extract_qualys_hosts

extract_crowdstrike_hosts.delay()
extract_qualys_hosts.delay()
```

Now you can connect to mongodb and see your results!

### using the development toolbox

**configure**

```sh
cd toolbox
make toolbox
make enter
cd $(git rev-parse --show-toplevel)
xc init
```

**configure your `.env` file!**

```sh
direnv reload
xc service-start
xc ipy
```

start the extraction manually

```py
from cq_pipe.tasks import extract_crowdstrike_hosts, extract_qualys_hosts

extract_crowdstrike_hosts.delay()
extract_qualys_hosts.delay()
```

Now you can connect to mongodb and see your results!

## Development

### Development-Prerequisites

While I attempt to provide all the tooling within a container, this requires a baseline installation and configuration of podman and distrobox.
See [the toolbox README](./toolbox/README.md) for additional instructions.

### Entry

From the `toolbox` directory, run `make toolbox` and `make enter` on the host to create/enter a development environment.

n.b. This will create a directory and file on your host for seemless integration with VSCode (my preferred editor) at:
`${HOME}/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/imageConfigs`

### First-time setup

From within the toolbox, run `xc init` to configure the pre-commit hook (see the task definition below!).

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
    --env RUN_LOCAL=true \
    --env FILTER_REGEX_EXCLUDE=".*mypy_cache/.*" \
    --env VALIDATE_ALL_CODEBASE=false \
    --volume "${GIT_DIR}":/tmp/lint \
    ghcr.io/super-linter/super-linter:slim-latest
```

### init

Initialize the repository with a shared git hook to enforce linting prior to commit.

```sh
cd $(git rev-parse --show-toplevel)
# configure the shared githook path
git config core.hooksPath .githooks
# write a default env file
cp .env.sample .env
direnv allow
# setup the virtual environment
poetry install --dev
```

### service-start

starts underlying containerized services

```sh
cd $(git rev-parse --show-toplevel)
podman compose up --detach --no-recreate
```

### start

starts a celery worker locally

requires: service-start

```sh
# ensure we've loaded the environment variables
cd $(git rev-parse --show-toplevel)
poetry run celery --app "cq_pipe" worker --loglevel INFO
```

### ipy

starts interactive python in the virtual environment

```sh
cd $(git rev-parse --show-toplevel)
poetry run python3
```

### test

executes python unittests

```sh
cd $(git rev-parse --show-toplevel)
poetry run python3 -m unittest
```

### run

runs the extract tasks to populate the database

requires: service-start

```sh
poetry run python3 run.py
```

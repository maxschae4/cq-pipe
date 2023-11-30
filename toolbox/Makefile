# toolbox container image name
toolbox_name := cq-pipe
# toolbox container image tag - using only "latest" for now
toolbox_tag := latest

# create the toolbox container
.PHONY: build
build:
	podman build --format docker \
		--file Containerfile \
		--tag $(toolbox_name):$(toolbox_tag) .

# primary entrypoint for creating the toolbox
# depends on rm and build targets to ensure we always "make" the toolbox
.PHONY: toolbox
toolbox: rm build
	distrobox assemble create --file distrobox.ini

# primary entry point for stepping into the toolbox
# avoids dependence on creating the toolbox/image for fast execution
.PHONY: enter
enter:
	distrobox enter $(toolbox_name)

# helper to enable stopping the toolbox in case it is left running
.PHONY: stop
stop:
	distrobox stop $(toolbox_name) || true

# helper to remove the distrobox in case we want to reset
.PHONY: rm
rm: stop
	distrobox rm $(toolbox_name) || true

# cleanup script that destroys the toolbox definition and the backing images
.PHONY: clean
clean: stop rm
	podman image rm $(toolbox_name) $(toolbox_name) || true

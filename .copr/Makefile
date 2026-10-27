spec ?= packages/falcond/falcond.spec
outdir ?= $(CURDIR)/srpm
.PHONY: srpm
srpm:
	@command -v git >/dev/null && command -v rpmbuild >/dev/null && command -v python3 >/dev/null || dnf -y install git rpm-build python3
	python3 .copr/build-srpm.py --spec '$(spec)' --outdir '$(outdir)'

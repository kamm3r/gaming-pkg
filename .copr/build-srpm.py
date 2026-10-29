import argparse, hashlib, io, json, pathlib, shutil, subprocess, tarfile, tempfile, urllib.request
parser = argparse.ArgumentParser()
parser.add_argument("--spec", required=True)
parser.add_argument("--outdir", required=True)
args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parent.parent
spec = pathlib.Path(args.spec).resolve()
name = spec.stem
assert spec == root / "packages" / name / (name + ".spec"), "Unknown recipe"
source = json.loads((root / "sources.json").read_text())[name]
version = subprocess.check_output(["rpmspec", "-q", "--srpm", "--qf", "%{VERSION}", str(spec)], text=True)
out = pathlib.Path(args.outdir).resolve()
out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["git", "init", "-q", tmp], check=True)
    subprocess.run(["git", "-C", tmp, "fetch", "-q", "--depth=1", source["url"], source["commit"]], check=True)
    actual = subprocess.check_output(["git", "-C", tmp, "rev-parse", "FETCH_HEAD"], text=True).strip()
    assert actual == source["commit"], "Source commit mismatch"
    archive = out / (name + "-" + version + ".tar.gz")
    prefix = name + "-" + version + "/"
    if source.get("submodules"):
        subprocess.run(["git", "-C", tmp, "checkout", "-q", "--detach", actual], check=True)
        subprocess.run(["git", "-C", tmp, "submodule", "update", "--init", "--recursive", "--depth=1"], check=True)
        # Each nested archive comes from the gitlink pinned by its parent,
        # rather than from a submodule branch or the working tree.
        def add_tree(destination, repo, commit, tree_prefix):
            data = subprocess.check_output(["git", "-C", str(repo), "archive", "--format=tar", "--prefix=" + tree_prefix, commit])
            with tarfile.open(fileobj=io.BytesIO(data)) as tree:
                for member in tree:
                    destination.addfile(member, tree.extractfile(member) if member.isfile() else None)
            entries = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-rz", commit])
            for entry in entries.split(b"\0"):
                if not entry:
                    continue
                metadata, path = entry.split(b"\t", 1)
                mode, kind, revision = metadata.decode().split()
                if mode == "160000":
                    subpath = path.decode()
                    subrepo = repo / subpath
                    checked = subprocess.check_output(["git", "-C", str(subrepo), "rev-parse", "HEAD"], text=True).strip()
                    assert checked == revision, "Submodule commit mismatch: " + subpath
                    add_tree(destination, subrepo, revision, tree_prefix + subpath + "/")
        with tarfile.open(archive, "w:gz") as destination:
            add_tree(destination, pathlib.Path(tmp), actual, prefix)
    else:
        subprocess.run(["git", "-C", tmp, "archive", "--format=tar.gz", "--prefix=" + prefix, "-o", str(archive), actual], check=True)
for extra in source.get("downloads", []):
    target = out / extra["filename"]
    with urllib.request.urlopen(extra["url"], timeout=120) as response, target.open("wb") as dest:
        shutil.copyfileobj(response, dest)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == extra["sha256"], "Download checksum mismatch"
subprocess.run(["rpmbuild", "-bs", "--define", "_sourcedir " + str(out), "--define", "_srcrpmdir " + str(out), str(spec)], check=True)

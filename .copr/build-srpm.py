import argparse, hashlib, json, pathlib, shutil, subprocess, tempfile, urllib.request
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
    subprocess.run(["git", "-C", tmp, "archive", "--format=tar.gz", "--prefix=" + name + "-" + version + "/", "-o", str(out / (name + "-" + version + ".tar.gz")), actual], check=True)
for extra in source.get("downloads", []):
    target = out / extra["filename"]
    with urllib.request.urlopen(extra["url"], timeout=120) as response, target.open("wb") as dest:
        shutil.copyfileobj(response, dest)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == extra["sha256"], "Download checksum mismatch"
subprocess.run(["rpmbuild", "-bs", "--define", "_sourcedir " + str(out), "--define", "_srcrpmdir " + str(out), str(spec)], check=True)

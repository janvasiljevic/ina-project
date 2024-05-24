import csv
import json
import re
import tarfile
import zipfile
from base64 import b64encode
from io import BytesIO

import requests
from tqdm import tqdm

response = requests.get("https://pypi.org/simple/")
html = response.text
packages = [match.group(1) for match in re.finditer(r'"/simple/([^/]+)/"', html)]




def _extract_deps(content):
    """Extract dependencies using install_requires directive"""
    # print("Extracting dependencies")
    # print(f'Content: {content}')
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    if isinstance(content, list):
        content = "".join(content)
    results = re.findall(r"install_requires=\[([\W'a-zA-Z0-9]*?)\]", content, re.M)
    deps = []
    if results:
        deps = [
            a.replace("'", "").strip()
            for a in results[0].strip().split(",")
            if a.replace("'", "").strip() != ""
        ]
    return deps


def _extract_setup_content(package_file):
    """Extract setup.py content as string from downladed tar"""
    if tarfile.is_tarfile(package_file):
        # tqdm.write("Extracting tar")
        tar_file = tarfile.open(fileobj=package_file)
        setup_candidates = [
            elem for elem in tar_file.getmembers() if "setup.py" in elem.name
        ]
        if len(setup_candidates) == 1:
            setup_member = setup_candidates[0]
            content = tar_file.extractfile(setup_member).read()
            deps = _extract_deps(content)
            return deps

        else:
            # tqdm.write("Too few candidates or too many for setup.py in tar")
            return None
    elif zipfile.is_zipfile(package_file):
        # tqdm.write("Extracting zip")
        zip_file = zipfile.ZipFile(package_file)
        metadata = [elem for elem in zip_file.namelist() if "METADATA" in elem]
        if metadata:
            content = zip_file.read(metadata[0]).decode("utf-8")
            requires = re.findall(r"^Requires-Dist:\s*([\w\-]+)", content, re.M)
            if requires:
                return requires
            return None
        setup_candidates = [elem for elem in zip_file.namelist() if "setup.py" in elem]
        if setup_candidates:
            setup_member = setup_candidates[0]
            content = zip_file.read(setup_member).decode("utf-8")
            # tqdm.write(f'setup.py: {content}')
            deps = _extract_deps(content)
            # tqdm.write(f'deps for zip setup.py: {deps}')
            return deps
        requires = [elem for elem in zip_file.namelist() if "requires.txt" in elem]
        if requires:
            content = zip_file.read(requires[0]).decode("utf-8")
            deps = content.split("\n")
            # tqdm.write(f'deps for zip requires.txt: {deps}')
            return deps
        # tqdm.write(f'Filenames: {zip_file.namelist()}')
        # tqdm.write("Too few candidates or too many for setup.py in zip")
        return None


csv_file = open("pypi-deps.csv", "w")
writer = csv.writer(csv_file, delimiter="\t", quotechar="|", quoting=csv.QUOTE_MINIMAL)


def extract_package(name):
    info = requests.get(
        f"https://pypi.org/pypi/{name}/json", headers={"Accept": "application/json"}
    ).json()
    releases = info.get("releases")
    if not releases:
        # tqdm.write(f"No releases found for {name}")
        return
    # only take the latest release
    version, release = list(releases.items())[-1]
    # tqdm.write("Extracting %s release %s" % (name, version) )
    if release:
        url = (
            release[0]
            .get("url")
            .replace("http://pypi.python.org/", "http://f.pypi.python.org/")
        )
        # tqdm.write("Downloading url %s" % url)
        req = requests.get(url)

        if req.status_code != 200:
            tqdm.write("Could not download file %s" % req.status_code)
        else:
            content = BytesIO(req.content)
            try:
                deps = _extract_setup_content(content)
            except Exception as e:
                tqdm.write(f"Error extracting setup.py content: {e}")
                deps = None
        if deps is None:
            deps = []
        writer.writerow([name, b64encode(json.dumps(deps).encode("utf-8")).decode("utf-8")])



# main processing
for package in (pbar := tqdm(packages, position=0, leave=True)):
    pbar.set_postfix_str(f"Processing {package}")
    extract_package(package)

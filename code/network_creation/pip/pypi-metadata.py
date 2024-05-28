import csv
import json
import re
import tarfile
import zipfile
from base64 import b64encode
from io import BytesIO
from joblib import Parallel, delayed

import requests
from tqdm import tqdm
import pandas as pd

response = requests.get("https://pypi.org/simple/")
html = response.text
packages = [match.group(1) for match in re.finditer(r'"/simple/([^/]+)/"', html)]

def split_list_into_parts(lst, num_parts):
    # Calculate the size of each part
    part_size = len(lst) // num_parts
    remainder = len(lst) % num_parts
    
    # Create the list of parts
    parts = []
    start = 0
    
    for i in range(num_parts):
        end = start + part_size + (1 if i < remainder else 0)  # distribute the remainder evenly
        parts.append(lst[start:end])
        start = end
    
    return parts

num_jobs = 8
# split into num_jobs arrays
len_per_job = len(packages) // num_jobs
package_batches = split_list_into_parts(packages, num_jobs)

test = packages[:100]
test_batched = split_list_into_parts(test, num_jobs)





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


def extract_package(name, results_list):
    try:
        info = requests.get(
            f"https://pypi.org/pypi/{name}/json", headers={"Accept": "application/json"}
        ).json()
    except:
        tqdm.write(f"Could not download metadata for {name}")
        return
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
        try:
            req = requests.get(url)
        except:
            tqdm.write(f"Could not download file {url} for {name}")
            return

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

        results_list.append([name, b64encode(json.dumps(deps).encode("utf-8")).decode("utf-8")])
        # writer.writerow([name, b64encode(json.dumps(deps).encode("utf-8")).decode("utf-8")])


def process_batch(batch):
    results = []
    for package in tqdm(batch):
        extract_package(package, results)
    results_df = pd.DataFrame(results, columns=["package", "deps"])
    return results_df

parallelized = Parallel(n_jobs=num_jobs, backend="threading")
results_par = parallelized(delayed(process_batch)(batch) for batch in package_batches)
results_merged = pd.concat(results_par)
results_merged.to_csv("pypi-deps.csv", sep="\t", index=False)

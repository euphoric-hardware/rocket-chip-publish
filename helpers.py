import subprocess
import fileinput
import sys
import urllib.request
from pathlib import Path
import re
from typing import List


def run_cmd(cmd: str, cwd: Path) -> subprocess.CompletedProcess:
    print(f"running {cmd}")
    result = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=cwd)
    assert result.returncode == 0, f"{cmd} failed with returncode {result.returncode}"
    return result

def run_cmd_capture(cmd: str, cwd: Path) -> str:
    print(f"running {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, cwd=cwd)
    stdout = result.stdout.decode('UTF-8').strip()
    assert result.returncode == 0, f"{cmd} failed with returncode {result.returncode} and stdout {stdout}"
    return stdout

version_re = re.compile(r'^\s*def publishVersion = T {')
lib_version_re = re.compile(r'^\s*def publishVersion = ')

def mill_sc_version(sc: List[str]) -> str:
    for idx, line in enumerate(sc):
        if 'Version' in line:
            match = version_re.match(line)
            if match is not None:
                version_str = sc[idx+1]
                version = version_str.strip()[1:-1]
                if any([x in version for x in ("SNAPSHOT", "-")]):
                    raise ValueError("rocket-chip version is a SNAPSHOT")
                return version
    raise ValueError("version not found in rocket-chip's build.sc")

def get_new_version(git_hash: str, rc_version: str) -> str:
    # construct the desired rocket-chip version as {OG version}-{rc hash}-SNAPSHOT
    return f"{rc_version}-{git_hash}-SNAPSHOT"

def replace_version_rc(sc: List[str], new_version: str) -> List[str]:
    new_sc: List[str] = []
    just_saw_version_line = False
    for line in sc:
        if "Version" in line and version_re.match(line) is not None:
            just_saw_version_line = True
            new_sc.append(line)
            continue
        elif just_saw_version_line:
            new_sc.append(f'"{new_version}"')
            just_saw_version_line = False
            continue
        else:
            new_sc.append(line)
    return new_sc

def replace_version_libs(sc: List[str], new_version: str) -> List[str]:
    new_sc: List[str] = []
    for line in sc:
        if "Version" in line and lib_version_re.match(line) is not None:
            new_sc.append(f'def publishVersion = "{new_version}"')
        else:
            new_sc.append(line)
    return new_sc

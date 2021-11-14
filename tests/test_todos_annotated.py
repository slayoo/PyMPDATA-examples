import pytest
import os
import re
import sys
import pathlib
from ghapi.all import GhApi, paged
from fastcore.net import ExceptionsHTTP


# https://stackoverflow.com/questions/7012921/recursive-grep-using-python
def findfiles(path, regex):
    reg_obj = re.compile(regex)
    res = []
    for root, _, fnames in os.walk(path):
        for fname in fnames:
            if reg_obj.match(fname):
                res.append(os.path.join(root, fname))
    return res


def grep(filepath, regex):
    reg_obj = re.compile(regex)
    res = []
    with open(filepath, encoding="utf8") as f:
        for line in f:
            if reg_obj.match(line):
                res.append(line)
    return res


@pytest.fixture(params=findfiles(pathlib.Path(__file__).parent.parent.absolute(), r'.*\.(ipynb|py|txt|yml|m|jl|md)$'))
def file(request):
    return request.param


@pytest.fixture(scope='session')
def gh_issues():
    res = {}
    if 'CI' not in os.environ or ('GITHUB_ACTIONS' in os.environ and sys.version_info.minor >= 8):
        try:
            api = GhApi(owner='atmos-cloud-sim-uj', repo='PyMPDATA')
            pages = paged(api.issues.list_for_repo, owner='atmos-cloud-sim-uj', repo='PyMPDATA', state='all', per_page=100)
            for page in pages:
                for item in page.items:
                    res[item.number] = item.state
        except ExceptionsHTTP[403]:
            pass
    return res


def test_todos_annotated(file, gh_issues):  # pylint: disable=redefined-outer-name
    if os.path.basename(file) == 'test_todos_annotated.py' or file.endswith("-checkpoint.ipynb") or ".eggs" in file:
        return
    for line in grep(file, r'.*TODO.*'):
        if line.count('"image/png":') > 0:
            continue
        match = re.search(r'TODO #(\d+)', line)
        if match is None:
            raise Exception(f"TODO not annotated with issue id ({line})")
        giving_up_with_hope_other_builds_did_it = len(gh_issues) == 0
        if not giving_up_with_hope_other_builds_did_it:
            number = int(match.group(1))
            if number not in gh_issues.keys():
                raise Exception(f"TODO annotated with non-existent id ({line})")
            if gh_issues[number] != 'open':
                raise Exception(f"TODO remains for a non-open issue ({line})")

import importlib.resources as pkg_resources

def get_version():
    with pkg_resources.open_text('ptus', 'VERSION.txt') as file:
        return file.read().strip()


def get_commit_hash():
    with pkg_resources.open_text('ptus', 'COMMIT_HASH.txt') as file:
        return file.read().strip()


def version():
    return 'ptus %s (commit %s)' % (get_version(), get_commit_hash())

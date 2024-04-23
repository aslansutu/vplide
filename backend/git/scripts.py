import pygit2


def initialize(path_to_directory, is_bare=False):
    repo = pygit2.init_repository(path_to_directory, is_bare)

    index = repo.index
    index.add_all()
    index.write()
    ref = "HEAD"
    author = pygit2.Signature("Alice Author", "alice@authors.tld")
    committer = pygit2.Signature("Cecil Committer", "cecil@committers.tld")
    message = "Initial commit"
    tree = index.write_tree()
    parents = []
    repo.create_commit(ref, author, committer, message, tree, parents)

    return repo


def getRepository(path):
    return pygit2.discover_repository(path)


def commit(repo_path, name, email, message=""):
    repository = pygit2.Repository(pygit2.discover_repository(repo_path))
    index = repository.index
    index.add_all()
    index.write()
    ref = repository.head.name
    author = pygit2.Signature(name, email)
    committer = pygit2.Signature(name, email)
    tree = index.write_tree()
    parents = [repository.head.target]
    repository.create_commit(ref, author, committer, message, tree, parents)
    return

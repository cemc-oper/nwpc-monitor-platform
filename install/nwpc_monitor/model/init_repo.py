import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../../../")
from nwpc_monitor.model import Owner, Repo

from .data import repo_list
from .init_owner import get_owner

def get_owner_by_name(owner_name, session):
    query = session.query(Owner).filter(Owner.owner_name==owner_name)
    owner = query.first()
    return owner

def create_repo(owner_id, repo_name, repo_type):
    repo = Repo()
    repo.owner_id = owner_id
    repo.repo_name = repo_name
    repo.repo_type = repo_type
    return repo


def init_repos(session):
    repos = []
    for a_record in repo_list:
        owner_name = a_record["owner_name"]
        repo_name = a_record["repo_name"]
        repo_type = a_record["repo_type"]

        owner = get_owner_by_name(owner_name, session)
        if owner is None:
            continue

        repos.append(create_repo(owner.owner_id, repo_name, repo_type))

    for repo in repos:
        session.add(repo)
    session.commit()


def get_repo(owner_id, repo_name, session):
    query = session.query(Repo).filter(Repo.owner_id == owner_id).filter(Repo.repo_name==repo_name)
    repo = query.first()
    return repo


def remove_repos(session):
    repos = []
    for a_record in repo_list:
        owner_name = a_record["owner_name"]
        repo_name = a_record["repo_name"]

        owner = get_owner_by_name(owner_name, session)
        if owner is None:
            continue
        repo  = get_repo(owner.owner_id, repo_name, session)
        if repo is None:
            continue
        repos.append(repo)

    for repo in repos:
        session.delete(repo)
    session.commit()
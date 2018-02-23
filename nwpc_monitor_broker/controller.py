# coding=utf-8
from flask import current_app
from nwpc_monitor_broker.database import db
from nwpc_monitor.model import Owner

from flask import json, request, jsonify,render_template, abort


@current_app.route('/')
def get_index_page():
    return render_template("index.html")


@current_app.route('/<owner>')
@current_app.route('/orgs/<owner>/<path:path>')
def get_owner_page(owner, path=None):

    query = db.session.query(Owner).filter(Owner.owner_name == owner)
    owner_object = query.first()

    if owner_object is None:
        return abort(404)

    if owner_object.owner_type == "org":
        return get_org_page(owner)
    elif owner_object.owner_type == "user":
        return get_user_page(owner, path=path)
    else:
        result = {'error':'wrong'}
        return jsonify(result)


def get_user_page(user, path=None):
    return render_template("user.html", user=user)


def get_org_page(org):
    return render_template("organization.html", org=org)


@current_app.route('/<owner>/<repo>')
@current_app.route('/<owner>/<repo>/')
def get_repo_page(owner, repo):
    return render_template('repo.html', owner=owner, repo=repo)


@current_app.route('/<no_static:owner>/<repo>/<path:path>')
def get_repo_path_page(owner, repo, path):
    return render_template('repo.html', owner=owner, repo=repo, path=path)
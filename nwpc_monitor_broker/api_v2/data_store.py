from nwpc_monitor_broker import app, db
from nwpc_monitor.model import Owner, Repo, DingtalkUser, DingtalkWarnWatch


def get_warn_user_list(owner: str, repo: str) -> list:
    query = db.session.query(Owner, Repo, DingtalkUser, DingtalkWarnWatch).filter(Repo.owner_id == Owner.owner_id)\
        .filter(Repo.repo_name == repo)  \
        .filter(Owner.owner_name == owner) \
        .filter(DingtalkWarnWatch.repo_id == Repo.repo_id) \
        .filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id)

    warn_to_user_list = []
    for (owner_object, repo_object, dingtalk_user_object, dingtalk_warn_watch_object) in query.all():
        userid = dingtalk_user_object.dingtalk_member_userid
        print(userid)
        warn_to_user_list.append(userid)

    return warn_to_user_list
from nwpc_monitor_web.app import mongodb_client

# mongodb
nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status
hpc_disk_usage_status = nwpc_monitor_platform_mongodb.hpc_disk_usage_status


def save_disk_usage_to_mongodb(user: str, value: dict) -> None:
    key = {
        "user": user
    }
    hpc_disk_usage_status.update(key, value, upsert=True)


def get_disk_usage_to_mongodb(user: str) -> dict:
    key = {
        'user': user
    }
    result = hpc_disk_usage_status.find_one(key, {"_id": 0})
    return result

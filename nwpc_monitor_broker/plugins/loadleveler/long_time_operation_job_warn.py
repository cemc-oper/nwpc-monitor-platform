# coding=utf-8
from collections import defaultdict
from nwpc_monitor_broker.plugins.loadleveler import loadleveler_filter
from nwpc_monitor.loadleveler.filter_condition import get_property_data

from nwpc_monitor_broker.api_v2.cache import redis_client


def save_long_time_operation_job_list_to_cache():
    pass


def get_long_time_operation_job_list_from_cache():
    pass


def warn_long_time_operation_job(message):
    job_items = message['data']['response']['items']
    filter_results = loadleveler_filter.apply_filters(job_items)
    long_time_result = filter_results[0]
    if len(long_time_result['target_job_items']) > 0:
        print("there is long time job in loadleveler")

        categorized_result = defaultdict(int)
        for a_job in long_time_result['target_job_items']:
            owner = get_property_data(a_job, "llq.owner")
            categorized_result[owner] += 1
        return {
            'categorized_result': categorized_result
        }
    else:
        return None

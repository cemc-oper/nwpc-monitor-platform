import datetime
from nwpc_monitor.loadleveler.filter_condition import \
    FilterCondition, \
    PropertyFilterCondition, \
    create_equal_value_checker


def create_job(
        id="id_no",
        owner="owner",
        job_class="job_class",
        queue_date=datetime.datetime.now()):
    return {
        "props": [
            {
                "id": "llq.id",
                "data": "llq.id" + id,
                "text": "llq.id" + id,
                "value": "llq.id" + id
            },
            {
                "id": "llq.owner",
                "data": owner,
                "text": owner,
                "value": owner
            },
            {
                "id": "llq.class",
                "data": job_class,
                "text": job_class,
                "value": job_class
            },
            {
                "id": "llq.job_script",
                "data": "llq.job_script" + id,
                "text": "llq.job_script" + id,
                "value": "llq.job_script" + id
            },
            {
                "id": "llq.status" + id,
                "data": "llq.status" + id,
                "text": "llq.status" + id,
                "value": "llq.status" + id
            },
            {
                "id": "llq.queue_date",
                "data": queue_date.strftime("%Y-%m-%d %H:%M:%S"),  # 2017-04-21 07:08:43
                "text": queue_date.strftime("%m/%d %H:%M"),  # "04/21 07:08",
                "value": queue_date.strftime("%a %b %d %H:%M:%S %Y"),  # "Fri Apr 21 07:08:43 2017"
            },
            {
                "id": "llq.priority",
                "data": id,
                "text": "llq.priority" + id,
                "value": "llq.priority" + id
            }
        ]
    }


def test_condition():
    condition = FilterCondition()
    job_item = dict()
    assert condition.is_fit(job_item)


def test_property_condition():
    job_item = create_job("id", "nwp_xp", "serial", datetime.datetime.now())

    condition = PropertyFilterCondition(
        property_id="llq.owner",
        data_checker=create_equal_value_checker("nwp_xp"))

    assert condition.is_fit(job_item)

    condition = PropertyFilterCondition(
        property_id="llq.owner",
        data_checker=create_equal_value_checker("unknown")
    )
    assert not condition.is_fit(job_item)

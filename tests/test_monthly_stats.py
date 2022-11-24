import requests
from app.config import Config
from scripts.monthly_stats import MonthlyStats
from nose.tools import assert_true

#  The email address below can be modified to check the emails are sending and look as expected
#  (using any email you control is fine as long as it is not pushed to github)

test_email_recipient = 'myname@domain.com'

test_data = {
    "0000-0002-3722-6351": {
        "datasets": [
            {
                "datasetId": 230,
                "version": 1,
                "origin": "SPARC",
                "downloads": 1
            },
            {
                "datasetId": 225,
                "version": 1,
                "origin": "SPARC",
                "downloads": 1
            },
            {
                "datasetId": 141,
                "version": 2,
                "origin": "SPARC",
                "downloads": 1
            }
        ],
        "email": test_email_recipient
    }
}

ms = MonthlyStats(debug_mode=True, debug_email=test_email_recipient)


def test_pennsieve_login():
    key = ms.pennsieve_login()
    r = requests.get(f"{Config.PENNSIEVE_API_HOST}/datasets",
                     headers={"Authorization": f"Bearer {key}"})
    assert_true(r.status_code == 200)


def test_metrics_endpoint():
    stats = ms.get_download_metrics_one_month()
    assert_true(len(stats) > 0)  # note this assumes there is at least one download a month


def test_stats_generation():
    stats = ms.get_stats()
    assert_true(len(stats.keys()) > 0)


def test_email():  # Note that this will send an email to the test_"email_recipient" provided at the top of this doc
    responses = ms.send_stats(test_data)
    if True in [r.status_code == 202 for r in responses]:
        print('Uh-oh, we have hit the sendgrid max email limit!')
    assert_true(False not in [r.status_code == 200 for r in responses])  # Check all responses were 200


def test_full_run():  # For each recipient, this will send an email to the test_email for each email that would have been sent to a user
    responses = ms.run()
    if True in [r.status_code == 202 for r in responses]:
        print('Uh-oh, we have hit the sendgrid max email limit!')
    assert_true(False not in [r.status_code == 200 for r in responses])

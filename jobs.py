from extensions import rq


@rq.job
def test_job():
    return

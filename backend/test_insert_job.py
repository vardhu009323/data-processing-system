
from models import Job


def test_insert_job(test_db_session):
    job = Job(
        status="completed",
        input_size=4,
        result={
            "maximum": 45,
            "minimum": 7,
            "sum": 87,
        },
    )

    test_db_session.add(job)
    test_db_session.commit()
    test_db_session.refresh(job)

    assert job.id is not None
    assert job.status == "completed"
    assert job.input_size == 4
    assert job.result == {
        "maximum": 45,
        "minimum": 7,
        "sum": 87,
    }

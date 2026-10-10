
from database import SessionLocal
from models import Job

session = SessionLocal()

try:
    job = Job(
        status="completed",
        input_size=4,
        result={
            "maximum": 45,
            "minimum": 7,
            "sum": 87
        }
    )

    session.add(job)
    session.commit()
    session.refresh(job)

    print("Job inserted successfully!")
    print("Job ID:", job.id)
    print("Result:", job.result)

except Exception:
    session.rollback()
    raise

finally:
    session.close()

from database import SessionLocal, Base, engine

session = SessionLocal()

print("Session created:", session is not None)
print("Base configured:", Base is not None)

session.close()
engine.dispose()
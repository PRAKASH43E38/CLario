from app.db.session import get_db
from app.models.learner import LearningSession, User
from sqlalchemy import text

# Check DB connection
engine = get_db().engine
print('DB URL:', engine.url)

# Check tables
with engine.connect() as conn:
    tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")).fetchall()
    print('Tables:', [t[0] for t in tables])

# Check sessions
with next(get_db()) as db:
    sessions = db.query(LearningSession).all()
    print('Sessions:', [(s.id, s.task, s.status) for s in sessions])
    users = db.query(User).all()
    print('Users:', [(u.id, u.email) for u in users])

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MovieAssistantBot.database.models import Base, SearchHistory
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "search_history.db")

engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

async def save_history(user_id: int, search_type: str, query: str):
    session = Session()
    entry = SearchHistory(user_id=user_id, search_type=search_type, query=query)
    session.add(entry)
    session.commit()
    session.close()

async def get_history(user_id: int) -> list[SearchHistory]:
    session = Session()
    history = session.query(SearchHistory).filter_by(user_id=user_id).order_by(SearchHistory.timestamp.desc()).limit(10).all()
    session.close()
    return history


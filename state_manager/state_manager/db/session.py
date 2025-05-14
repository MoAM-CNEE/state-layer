from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseSessionManager:
    def __init__(self):
        user = quote_plus("root")
        password = quote_plus("hunter2")
        host = "state-persister-svc.state-layer.svc.cluster.local"
        port = 3306
        db_name = "state_persister_db"

        self.connection_string = (
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        )
        self.engine = create_engine(self.connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

from abc import ABC, abstractmethod
import mysql.connector

from schemas.retrieve import RetrieveRQ, RetrieveRS


class SystemEntityService(ABC):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='state-persister-svc.state-layer.svc.cluster.local',
            port=3306,
            user='root',
            password='hunter2'
        )
        self.cursor = self.conn.cursor()
        db_name = 'state_persister_db'
        self.cursor.execute(f"USE {db_name}")

    def run_query(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    @abstractmethod
    def persist(self):
        pass

    @abstractmethod
    def retrieve(self, retrieve_rq: RetrieveRQ) -> RetrieveRS:
        pass

from sqlalchemy import text, insert, select, update
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersOrm


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True
        
    @staticmethod    
    def insert_workers():
        with session_factory() as session:
            worker_jack= WorkersOrm(username="Jack")
            worker_michael=WorkersOrm(username="Michael")
            session.add_all([worker_jack, worker_michael])
            session.flush()
            session.commit()
        
        
    @staticmethod
    def select_workers():
        with session_factory() as session:
            #worker _id = 1
            #worker_jack = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm) # SELECT * FROM workers
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers =}")
            
    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersOrm, worker_id)
            worker_michael.username = new_username
            session.expire_all()
            session.commit()
    
    
    
    
    
    
    
    
    
    async def insert_data():
        async with async_session_factory() as session:
            worker_bobr= WorkersOrm(username="Bobr")
            worker_volk=WorkersOrm(username="Volk")
            session.add_all([worker_bobr, worker_volk])
            await session.commit()
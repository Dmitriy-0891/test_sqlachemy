from sqlalchemy import and_, text, insert, select, update, Integer, cast, func
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersOrm, ResumeOrm, Workload


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
            session.refresh(worker_michael)
            session.commit()
    
    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumeOrm(
                title= 'Python Junior Developer',
                compensation = 50000,
                workload = Workload.fulltime,
                worker_id = 1
            )
            resume_jack_2 = ResumeOrm(
                title= 'Python Разработчик',
                compensation = 150000,
                workload = Workload.fulltime,
                worker_id = 1
            )
            resume_michael_1 = ResumeOrm(
                title= 'Python Data Engineer',
                compensation = 250000,
                workload = Workload.parttime,
                worker_id = 2
            )
            resume_michael_2 = ResumeOrm(
                title= 'Data Scientist',
                compensation = 300000,
                workload = Workload.fulltime,
                worker_id = 2
            )
            session.add_all([resume_jack_1, resume_jack_2,
                             resume_michael_1, resume_michael_2])
            session.commit()
            sync_engine.echo = True
            
    @staticmethod
    def select_resumes_avg_compensation(like_language: str = 'Python'):
        with session_factory() as session:
            query = (
                select(
                    ResumeOrm.workload,
                    cast(func.avg(ResumeOrm.compensation), Integer).label("avg_compesation")
                )
                .select_from(ResumeOrm)
                .filter(and_(
                    ResumeOrm.title.contains(like_language),
                    ResumeOrm.compensation > 40000,
                ))
                .group_by(ResumeOrm.workload)
                .having(cast(func.avg(ResumeOrm.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds":True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compesation)
            
    
    
    
    
    
    
    
    async def insert_data():
        async with async_session_factory() as session:
            worker_bobr= WorkersOrm(username="Bobr")
            worker_volk=WorkersOrm(username="Volk")
            session.add_all([worker_bobr, worker_volk])
            await session.commit()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from settings import engine

Base = declarative_base()


class Video(Base):
    __tablename__ = 'video'

    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    url = Column(String(255))
    duration_in_seconds = Column(Integer)
    views = Column(Integer)
    thumbnail_image_path = Column(String(255))
    thumbnail_image_url = Column(String(255))
    fullsized_image_path = Column(String(255))
    fullsized_image_url = Column(String(255))

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    @classmethod
    def save(cls, videos):
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add_all(videos)
        session.commit()
        session.close()

        print("Objects saved successfully :)")

    @classmethod
    def update(cls, videos):
        Session = sessionmaker(bind=engine)
        session = Session()
        for video in videos:
            session.query(Video).filter(Video.id == video.id).update(
                {column: getattr(video, column) for column in Video.__table__.columns.keys()},
                synchronize_session=False)
        session.commit()
        session.close()

        print("Objects updated successfully :)")

    @classmethod
    def save_or_update(cls, videos):
        Session = sessionmaker(bind=engine)
        session = Session()
        new_videos = []
        for video in videos:
            entry = session.query(Video).filter(Video.id == video.id).first()
            if entry:
                session.query(Video).filter(Video.id == video.id).update(
                    {column: getattr(video, column) for column in Video.__table__.columns.keys()})
            else:
                new_videos.append(video)

        session.add_all(new_videos)
        session.commit()
        session.close()

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine, tables=[Base.metadata.tables["video"]])

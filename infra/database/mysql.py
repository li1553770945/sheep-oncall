from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from infra.config.config_loader import Config

def database_provider(config:Config):


    # 创建引擎
    engine = create_engine(
        config.get("database","dsn"),
        # 超过链接池大小外最多创建的链接
        max_overflow=0,
        # 链接池大小
        pool_size=5,
        # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
        pool_timeout=10,
        # 多久之后对链接池中的链接进行一次回收
        pool_recycle=1,
        # 查看原生语句（未格式化）
        echo=True
    )

    # 绑定引擎
    Session = sessionmaker(bind=engine)
    # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
    # 内部会采用threading.local进行隔离
    session = scoped_session(Session)
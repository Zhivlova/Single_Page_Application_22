from sqlalchemy import create_engine, Table, Column, BigInteger, String, MetaData, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime


# Класс - серверная база данных:
class ServerStorage:
    class Items:
        def __init__(self, title):
            self.title = title

    class Parameters:
        def __init__(self, created_at, date, quantity, distance):
            self.title = created_at
            self.title = date
            self.title = quantity
            self.title = distance

    class ItemsParameters:
        def __init__(self, title, parameter):
            self.id = None
            self.title = title
            self.parameter = parameter

    def __init__(self):
        self.database_engine = create_engine("mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4",
                                             echo=False, pool_recycle=7200)
        self.metadata = MetaData()

        items_table = Table('Items', self.metadata,
                            Column('id', BigInteger(), primary_key=True),
                            Column('title', String(255), nullable=False, unique=True)
                            )
        parameters_table = Table('Parameters', self.metadata,
                                 Column('id', BigInteger(), primary_key=True),
                                 Column('created_on', DateTime(), default=datetime.utcnow),
                                 Column('updated_on', DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
                                 Column('date', Date()),
                                 Column('quantity', BigInteger()),
                                 Column('distance', BigInteger())
                                 )
        items_parameters = Table('ItemsParameters', self.metadata,
                                 Column('id', BigInteger(), primary_key=True),
                                 Column('item', ForeignKey('Items.id')),
                                 Column('parameter', ForeignKey('Items.id'))
                                 )
        self.metadata.create_all(self.database_engine)
        mapper(self.Items, items_table)
        mapper(self.Parameters, parameters_table)
        mapper(self.ItemsParameters, items_parameters)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.commit()

    def items_list(self):
        query = self.session.query(
            self.Items.title
        )
        return query.all()

    def get_items(self, username):

        title = self.session.query(self.Items).filter_by(name=id).one()

        query = self.session.query(self.ItemsParameters, self.Items.name). \
            filter_by(user=title.id). \
            join(self.Items, self.ItemsParameters.item == self.Items.id)

        # выбираем только имена пользователей и возвращаем их.
        return [item[1] for item in query.all()]


from copy import deepcopy
from pymysql import connect
from quopri import decodestring
from patterns.behavioral_patterns import FileWriter
from patterns.architectural_system_pattern_unit_of_work import DomainObject


# абстрактная таблица
class SomeTable:
    def __init__(self, name):
        self.name = name


# столбец
class Column(SomeTable):
    pass


# поле
class Field(SomeTable, DomainObject):
    def __init__(self, name):
        self.tables = []
        super().__init__(name)


class SomeTableFactory:
    types = {
        'column': Column,
        'field': Field
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


""""
Создание прототипов 
"""


# порождающий паттерн Прототип
class TablePrototype:
    # прототип услуги
    def clone(self):
        return deepcopy(self)


# абстрактная таблица
class Table(TablePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.tables.append(self)
        self.fields = []
        super().__init__()

    def __getitem__(self, item):
        return self.fields[item]

    def add_field(self, field: Field):
        self.fields.append(field)
        field.tables.append(self)
        self.notify()


""""
Создание категорий
"""


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.tables = []

    def table_count(self):
        result = len(self.tables)
        if self.category:
            result += self.category.table_count()
        return result


""""
Основной интерфейс проекта
"""


class Engine:
    def __init__(self):
        self.columns = []
        self.fields = []
        self.tables = []
        self.categories = []

    @staticmethod
    def create_table(type_):
        return SomeTableFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def get_table(self, name):
        for item in self.tables:
            if item.name == name:
                return item
        return None


    def get_field(self, name) -> Field:
        for item in self.fields:
            if item.name == name:
                return item


@staticmethod
def decode_value(val):
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = decodestring(val_b)
    return val_decode_str.decode('UTF-8')


class FieldMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'field'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            field = Field(name)
            field.id = id
            result.append(field)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Field(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)





# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'field': FieldMapper,
        # 'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Field):
            return FieldMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)

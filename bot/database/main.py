import pymysql
from bot.misc import dbKeys

class db:

    def __init__(self):
        '''Инициализация соединения с БД'''
        self.conn = pymysql.connect(host=dbKeys.host,
                                    port=3306, user=dbKeys.user,
                                    password=dbKeys.password,
                                    database=dbKeys.db_name,
                                    cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        '''Создание таблиц'''
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users 
            (
            id int PRIMARY KEY AUTO_INCREMENT, 
            user_id int NOT NULL
            );
            '''
        )
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS operations
            (
            id int PRIMARY KEY AUTO_INCREMENT,
            user_id int NOT NULL REFERENCES users (id) ON DELETE CASCADE,
            operation_type varchar(1) NOT NULL,
            first_number double NOT NULL,
            second_number double NOT NULL,
            answer double NOT NULL
            );
            '''
        )
        return self.conn.commit()

    def user_exists(self, user_id):
        '''Проверяем, есть ли уже пользователь в БД'''
        self.cursor.execute('''SELECT id FROM users WHERE user_id = %s''', (user_id,))
        return bool(len(self.cursor.fetchall()))

    def add_user(self, user_id):
        '''Добавляем пользователя в БД'''
        self.cursor.execute('''INSERT INTO users (user_id) VALUES (%s)''', (user_id,))
        return self.conn.commit()

    def add_operation(self, user_id, operation_type, first_number, second_number, answer):
        '''Добавляем операцию'''
        self.cursor.execute('''INSERT INTO operations 
        (user_id, operation_type, first_number, second_number, answer) 
        VALUES (%s, %s, %s, %s, %s)''', (user_id, operation_type, first_number, second_number, answer,))
        return self.conn.commit()

    def get_all_user_operations(self, user_id):
        '''Получаем все опреации пользователя'''
        self.cursor.execute('''SELECT * FROM operations WHERE user_id = %s''', (user_id,))
        return self.cursor.fetchall()
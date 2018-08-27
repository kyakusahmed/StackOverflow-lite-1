import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            "dbname='clvx' user='postgres' host='localhost' password='Password/123' port='5432'"
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

        except:
            print("Cannot connect to database.")

        def create_Users_table(self):
            self.tablename = 'users'
            create_table_command = """CREATE TABLE users(
                id serial PRIMARY KEY,
                username varchar(100) NOT NULL,
                password_hash varchar(200) NOT NULL,
                user_id varchar(150) NOT NULL
            )"""
            self.cursor.execute(create_table_command)

        def create_Questions_table(self):
            self.tablename = 'questions'
            create_table_command = """CREATE TABLE questions(
                id serial PRIMARY KEY,
                topic varchar(100) NOT NULL,
                body varchar(600) NOT NULL,
                question_id varchar(150) NOT NULL
            )"""
            self.cursor.execute(create_table_command)

        def create_Answer_table(self):
            self.tablename = 'answers'
            create_table_command = """CREATE TABLE answers(
                id serial PRIMARY KEY,
                Qn_Id varchar(150) NOT NULL,
                body varchar(600) NOT NULL,
                answer_id varchar(150) NOT NULL
            )"""
            self.cursor.execute(create_table_command)

        def insert_new_record(self, tablename, data):
            tables = ['users', 'questions', 'answers']
            if tablename == tables[0]:
                insert_command = f'''INSERT INTO {tables[0]}(
                    name,
                    password_hash,
                    user_id
                ) VALUES(
                    data['username'],
                    data['password_hash'],
                    data['user_id']
                )'''
            elif tablename == tables[1]:
                insert_command = f'''INSERT INTO {tables[1]}(
                    topic,
                    body,
                    question_id
                ) VALUES(
                    data['topic'],
                    data['body'],
                    data['question_id']
                )'''
            elif tablename == tables[2]:
                insert_command = f'''INSERT INTO {tables[2]}(
                    Qn_Id,
                    body,
                    answer_id
                ) VALUES(
                    data['Qn_Id'],
                    data['body'],
                    data['answer_id']
                )'''
            else:
                if tablename not in tables:
                    msg = f"""User table {tablename} does not exit."""
                    return msg

            def query_all(self, tablename):
                self.cursor.execute(f"SELECT * FROM {tablename}")
                items = self.cursor.fetchall()
                return items

            def update_table(self, tablename, variable,
                             current_value, new_value, identifier, id_value):
                update_command = f"""UPDATE {tablename}
                                 SET {variable} = {current_value}
                                 WHERE {identifier} = {id_value}"""
                self.cursor.execute(update_command)
            
            def update_table(self, tablename, variable,
                             current_value, new_value, identifier, id_value):
                update_command = f"""UPDATE {tablename}
                                 SET {variable} = {current_value}
                                 WHERE {identifier} = {id_value}"""
                self.cursor.execute(update_command)
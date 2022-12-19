import mysql
from mysql.connector import connect


class Database:
    """
    Класс с функциями для взаимодействия с базой данных
    """
    def __init__(self):
        """
        Подключение к базе данных MySQL
        """
        self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='user15')

    def insert_service(self, name, code, cost):
        """
        Добавление новой услуги
        :param name: наименование услуги
        :param code: код услуги
        :param cost: стоимость руб. за час
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO service VALUES (NULL, %s, %s, %s)", (name, code, cost))
        self.conn.commit()

    def insert_request(self, number, date, time, client, employee, service):
        """
        Добавление нового заказа
        :param number: номер заказа
        :param date: дата создания
        :param time: время создания
        :param client: номер клиента
        :param service: услуги
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO request VALUES (NULL, %s, %s, %s, %s, %s, NULL, NULL, NULL, %s)", (number, date, time, client, service, employee))
        self.conn.commit()

    def update_service(self, id, name, code, cost):
        """
        Обновление услуг
        :param id: id услуги
        :param name: наименование услуги
        :param code: код услуги
        :param cost: стоимость руб. за час
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE service set NameService='{name}', Code='{code}', Cost='{cost}' WHERE ID_Service='{id}'")
        self.conn.commit()

    def delete_service(self, id):
        """
        Удаление услуги
        :param id: id услуги
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM service WHERE ID_Service='{id}'")
        self.conn.commit()

    def select_clients(self):
        """
        Получение списка клиентов
        :return: rows
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM client")
        rows = cursor.fetchall()
        return rows

    def select_employees(self):
        """
        Получение списка сотрудников
        :return: rows
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM employee")
        rows = cursor.fetchall()
        return rows

    def select_services(self):
        """
        Получение списка услуг
        :return: rows
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM service")
        rows = cursor.fetchall()
        return rows

    def get_info(self, login):
        """
        Получение информации о сотруднике
        :param login: логин сотрудника
        :return: log
        """
        log = []
        fio = ''
        temp = 0
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT Password, Post, LastEnter, TypeEnter, Surname, Name, LastName, Photo, ID_Employee FROM employee WHERE Login = '{login}'""")
        rows = cursor.fetchall()

        for i in rows:
            for j in i:
                if temp == 4 or temp == 5 or temp == 6:
                    fio += j
                    if temp == 4 or temp == 5:
                        fio += ' '
                    if temp == 6:
                        log.append(fio)
                    temp += 1
                else:
                    log.append(str(j))
                    temp += 1
        return log

    def get_logins(self):
        """
        Получение списка логинов сотрудников
        :return: logins
        """
        logins = []
        cursor = self.conn.cursor()
        cursor.execute(f"""SELECT Login FROM employee""")
        rows = cursor.fetchall()

        for i in rows:
            for j in i:
                logins.append(j)
        return logins

    def get_clients(self):
        """
        Получение списка ФИО клиентов
        :return: clients
        """
        clients = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT Surname, Name, LastName FROM client")
        rows = cursor.fetchall()

        for i in rows:
            clients.append(str(i[0] + ' ' + i[1] + ' ' + i[2]))
        return clients

    def insert_client(self, surname, name, lastname, passportData, dateOfBirth, address, email):
        """
        Добавление нового клиента
        :param fio: ФИО
        :param passportData: Паспортные данные
        :param dateOfBirth: Дата рождения
        :param address: Адрес
        :param email: E-mail
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO client VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", (surname, name, lastname, passportData, dateOfBirth, address, email))
        self.conn.commit()

    def get_services(self):
        """
        Получение списка наименований услуг
        :return: services
        """
        services = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT NameService FROM service")
        rows = cursor.fetchall()

        for i in rows:
            services.append(str(i)[2:-3])
        return services

    def get_serv_id(self, name):
        """
        Получение кода услуги
        :param name: Наименование услуги
        :return: row
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT ID_Service FROM service WHERE NameService ='{name}'")
        row = str(cursor.fetchone())
        return row[1:-2]

    def get_client_id(self, surname, name, lastname):
        """
        Получение кода клиента
        :param fio: ФИО
        :return: row
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT ID_Client FROM client WHERE Surname='{surname}' and Name='{name}' and LastName='{lastname}'")
        row = str(cursor.fetchone())
        return row[1:-2]

    def insert_time_entry(self, id, time, success):
        """
        Добавление времени входа сотрудника
        :param login: Логин
        :param time: Дата и время
        :param success: успешная или ошибочная попытка входа
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute(f"INSERT INTO history VALUES (NULL, %s, NULL, %s, %s)", (time, success, id))
        cursor.execute(f"UPDATE employee set LastEnter='{time}', TypeEnter='{success}' WHERE ID_Employee='{id}'")
        self.conn.commit()

    def insert_time_exit(self, id, time, block):
        """
        Добавление времени входа сотрудника
        :param login: Логин
        :param time: Дата и время
        :param block: нужен ли блок
        :return: None
        """
        cursor = self.conn.cursor()
        cursor.execute(f"INSERT INTO history VALUES (NULL, NULL, %s, %s, %s)", (time, block, id))
        self.conn.commit()

    def select_history(self):
        """
        Получение истории входа сотрудников
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT DateOfEnter, DateOfExit, Block, Login FROM history INNER JOIN employee ON employee.ID_Employee = History.Employee")
        rows = cursor.fetchall()
        return rows

    def get_date_serv(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT Service, DateOfCreate FROM request")
        rows = cursor.fetchall()
        return rows

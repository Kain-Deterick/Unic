import mysql.connector

class DB():
    # Конструктор: для инициальзации и присвоение значений переменных класса
    def __init__(self):
        try:
            self.dataBase = mysql.connector.connect(
                host = 'localhost',
                port = 3306,
                user = 'Kain',
                password= 'Uxninitcroom13',
                database= 'unic'
            )
        except mysql.connector.Error as e:
            print(e)

    # Деструктор: при уничтожении объекта класса или завершении программы разрывает соединение
    def __del__(self):
        self.dataBase.close()

    # Чтение базы данных
    def select_table (self):
        selectAll = "SELECT * FROM kursach"
        with self.dataBase.cursor() as cursorObject:
            cursorObject.execute(selectAll)
            myResult = cursorObject.fetchall()
            return myResult

result = DB().select_table()

for row in result:
    print(row)


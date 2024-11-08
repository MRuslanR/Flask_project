import mysql.connector

def get_db_connection(database):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="MRuslanR",
            passwd="123456",
            database=database,
        )
    except Exception as e:
        print(f"Не удалось подключиться к базе данных {database}\nВозникла ошибка: {e}")
        quit()
    else:
        print(f"Успешное подключение к базе данных {database}")
        return connection
    # Disconnecting from the server
    #dataBase.close()

def insert_user(dataBase, username, email, password):
    cursorObject = dataBase.cursor()
    sql = "INSERT INTO users (username, email, password)\
           VALUES (%s, %s, %s)"
    val = (username, email, password)

    cursorObject.execute(sql, val)
    dataBase.commit()
    print(f'Added user {username}')



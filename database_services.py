from sqlalchemy import MetaData, Table, Column, String, create_engine, text

engine = create_engine('sqlite:///database.db', echo=True)

def create_tables():
    meta = MetaData()
    user = Table(
        'users', meta, 
        Column('name', String),
        Column('email', String, primary_key=True),
        Column('password', String)
    )

    meta.create_all(engine)

"""
    Get email and password and compare
"""
def db_login(email, password):
    connection = engine.connect()
    
    #   declare a schema for `users` table
    meta = MetaData()
    user = Table(
        'users', meta, 
        Column('name', String),
        Column('email', String, primary_key=True),
        Column('password', String)
    )

    """ SELECT all users """
    #   allUsers = a statement that states that we want to get all users
    # allUsers = user.select()

    #   here we actually get all users from the database 
    # result = connection.execute(allUsers)
    # for row in result:
    #     print(row)

    """ SELECT email & password that equals to the arguments """
    statement = text(f"SELECT * from users WHERE email = '{email}' AND password = '{password}'")

    selectedUser = connection.execute(statement).all()
    if len(selectedUser) == 1:
        return True
    return False

def db_create_user(name, email, password):
    connection = engine.connect()
    
    #   declare a schema for `users` table
    meta = MetaData()
    user = Table(
        'users', meta, 
        Column('name', String),
        Column('email', String, primary_key=True),
        Column('password', String)
    )

    """ INSERT new record into the table `users` """
    statement = text(f"INSERT INTO users(name, email, password) VALUES('{name}', '{email}', '{password}')")

    try:
        connection.execute(statement)
        return True
    except Exception:
        return False

def db_delete_user(email):
    connection = engine.connect()
    
    #   declare a schema for `users` table
    meta = MetaData()
    user = Table(
        'users', meta, 
        Column('name', String),
        Column('email', String, primary_key=True),
        Column('password', String)
    )

    """ DELETE a user record from `users` table by email"""
    statement = text(f"DELETE FROM users WHERE email = '{email}'")

    try:
        connection.execute(statement)
        print("Delete success")
        return True
    except Exception:
        print("Delete failed")
        return False

# if __name__ == '__main__':
    # create_tables()
    # login('long@example.com', '123456')
    # create_user('vu', 'vu@example.com', 'abcxyz')
    # delete_user('a')
import sqlite3
from sqlite3 import Error

program_password_set = "123"
web_address = ""
user_id = ""
user_password = ""

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

def execute_query(conn, cerate_table_sql):
    try:
        c = conn.cursor()
        c.execute(cerate_table_sql)
    except Error as e:
        print(e)

def login():
    program_password = input("Please enter the password: ")

    if program_password == program_password_set:
        return True
    else:
        return False

def check_input_valid():
    global web_address
    global user_id
    global user_password
    while True:
        if web_address == "":
            web_address = input("Enter web address: ")
        elif user_id == "":
            user_id = input("Enter your login id: ")
        elif user_password == "":
            user_password = input("Enter your login password: ")
        else:
            return True

def main():
    database = r"Password_Database.db"
    sql_create_id_password_table = """ 
    CREATE TABLE IF NOT EXISTS id_password (
        id integer PRIMARY KEY AUTOINCREMENT,
        login_id text NOT NULL,
        login_password text NOT NULL,
        website_adderss text NOT NULL
    );
    """
    
    conn = create_connection(database)

    if conn is not None:
        execute_query(conn, sql_create_id_password_table)
    else:
        print("Cannot create the database connection")

    login_pass = login()

    if login_pass:
        while True:
            print("1. Add login information")
            print("2. Edit login information")
            print("3. view all login information")
            choose = input("Enter your choose: ")
            if choose == "1":
                if check_input_valid():
                    print(user_id)
            else:
                break
    else:
        exit()



if __name__ == '__main__':
    main()
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

def execute_query(conn, query, task = None):
    try:
        c = conn.cursor()
        if task is None:
            c.execute(query)
        else:
            c.execute(query, task)
        conn.commit()
    except Error as e:
        print(e)

def execute_read_query(conn, query):
    result = None
    try:
        c = conn.cursor()
        c.execute(query)
        result = c.fetchall()
        return result
    except Error as e:
        print(e)

def login():
    program_password = input("\nPlease enter the password: ")

    if program_password == program_password_set:
        return True
    else:
        return False

def check_input_valid(web, u_id, u_pass):
    global web_address
    global user_id
    global user_password
    while True:
        print()
        if (web_address == "") & web:
            web_address = input("Enter web address: ")
        elif (user_id == "") & u_id:
            user_id = input("Enter your login id: ")
        elif (user_password == "") & u_pass:
            user_password = input("Enter your login password: ")
        else:
            return True

def reset_val():
    global web_address
    global user_id
    global user_password
    web_address = 0
    user_id = 0
    user_password = 0

if __name__ == '__main__':
    database = r"Password_Database.db"
    sql_create_id_password_table = """ 
    CREATE TABLE IF NOT EXISTS id_password (
        id integer PRIMARY KEY AUTOINCREMENT,
        login_id text NOT NULL,
        login_password text NOT NULL,
        website_address text NOT NULL
    );
    """
    
    conn = create_connection(database)

    if conn is not None:
        execute_query(conn, sql_create_id_password_table)
    else:
        print("\nCannot create the database connection")

    login_pass = login()

    if login_pass:
        while True:
            print("\nMain Menu")
            print("1. Add login information")
            print("2. Edit login information")
            print("3. view all login information")
            print("4. Quit")
            choose = input("\nEnter your choose: ")
            if choose == "1":
                if check_input_valid(True, True, True):
                    create_login_info = """
                    INSERT INTO
                        id_password(login_id, login_password, website_address)
                    VALUES
                        (?,?,?)
                    """
                    create_login_info_val = (user_id, user_password, web_address)
                    if conn is not None:
                        execute_query(conn, create_login_info, create_login_info_val)
                        reset_val()
                        print("\nLogin information added")
                    else:
                        print("\nCannot insert the info")
            elif choose == "2":
                view_all_login_info = """
                SELECT * FROM id_password
                """
                if conn is not None:
                    infos = execute_read_query(conn, view_all_login_info)
                web_of_database = input("\nEnter the website name: ")
                count = 0
                get_list = []
                for info in infos:
                    if web_of_database in info[3]:
                        count += 1
                        get_list.append(info[0])
                        print("\nNumber: " + str(count))
                        print("ID: " + str(info[0]))
                        print("web address: " + info[3])
                        print("login id: " + info[1])
                        print("login password: " + info[2])
                if count != 1:
                    input_number = input("\nEnter the number: ")
                else:
                    input_number = 1
                print("\nEdit menu")
                print("1. Edit all")
                print("2. Edit login id")
                print("3. Edit login password")
                print("4. Edit website address")
                print("5. Quit")
                edit_number = input("\nEnter the number: ")
                if (int(edit_number) <= 4) & (count != 0) & (int(input_number) <= len(get_list)):
                    if edit_number == "1":
                        edit_all = """
                        UPDATE id_password
                        SET login_id = ?
                            login_password = ?
                            website_address = ?
                        WHERE id = ?
                        """
                        check_input_valid(True, True, True)
                        edit_all_val = (user_id, user_password, web_address, get_list[input_number - 1])
                        if conn is not None:
                            execute_query(conn, edit_all, edit_all_val)
                            print("Login information updated")
                    elif edit_number == "2":
                        edit_login_id = """
                        UPDATE id_password
                        SET login_id = ?
                        WHERE id = ?
                        """
                        check_input_valid(False, True, False)
                        edit_login_id_val = (user_id, get_list[input_number - 1])
                        if conn is not None:
                            execute_query(conn, edit_login_id, edit_login_id_val)
                            print("Login id updated")
                    elif edit_number == "3":
                        edit_password = """
                        UPDATE id_password
                        SET login_password = ?
                        WHERE id = ?
                        """
                        check_input_valid(False, False, True)
                        edit_password_val = (user_password, get_list[input_number - 1])
                        if conn is not None:
                            execute_query(conn, edit_password, edit_password_val)
                            print("Login password updated")
                    elif edit_number == "4":
                        edit_web = """
                        UPDATE id_password
                        SET website_address = ?
                        WHERE id = ?
                        """
                        check_input_valid(True, False, False)
                        edit_web_val = (web_address, get_list[input_number - 1])
                        if conn is not None:
                            execute_query(conn, edit_web, edit_web_val)
                            print("Web address updated")
                    else:
                        print("Quit")

            elif choose == "3":
                view_all_login_info = """
                SELECT * FROM id_password
                """
                if conn is not None:
                    infos = execute_read_query(conn, view_all_login_info)
                    i = 0
                    for info in infos:
                        i += 1
                        print("\nrecord: " + str(i))
                        print("ID: " + str(info[0]))
                        print("web address: " + info[3])
                        print("login id: " + info[1])
                        print("login password: " + info[2])
                else:
                    print("\nCannot view the info")
            else:
                print("\nProcess end")
                break
    else:
        exit()
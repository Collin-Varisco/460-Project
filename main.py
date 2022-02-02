import sqlite3

""" Try to establish a connection with the database """
def create_connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
        return con
    except ValueError as e:
        print(e)
    return con


""" create a table from the createSqlTable statement
:param conn: Connection object
:param createSqlTable: a CREATE TABLE statement
:return:
"""
def createTable(conn, createSqlTable):
    try:
        c = conn.cursor()
        c.execute(createSqlTable)
    except ValueError as e:
        print(e)

def insertEmployee(conn):
    try:
        print("--- Insert Employee Information ---")
        eid = input("Employee ID: ")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        pos = input("Position: ")
        fid = input("Franchise ID: ")
        employeeSql = """INSERT INTO Employee
                         (EmpID, Fname, Lname, Position, FID )
                         VALUES (?, ?, ?, ?, ?);"""
        tuple = (eid, fname, lname, pos, fid)
        c = conn.cursor()
        c.execute(employeeSql, tuple)
        conn.commit()
        c.close()
    except sqlite.Error as error:
        print("//")
        print(error)
    finally:
        if conn:
            conn.close()
            print("Connection is closed.")

def addFranchise(conn):
    try:
        print("--- Add Franchise Information ---")
        fid = input("Franchise ID: ")
        streetAddress = input("Street Address: ")
        city = input("City: ")
        state = input("State: ")
        zipCode = input("Zip Code: ")
        ownerFname = input("Owner's First Name: ")
        ownerLname = input("Owner's Last Name: ")
        franchiseSql = """INSERT INTO Franchise
                         (FID, StreetAddress, City, State, ZipCode, OwnerFname, OwnerLname)
                         VALUES (?, ?, ?, ?, ?, ?, ?);"""
        f_tuple = (fid, streetAddress, city, state, zipCode, ownerFname, ownerLname)
        c = conn.cursor()
        c.execute(franchiseSql, f_tuple)
        conn.commit()
        c.close()
    except sqlite.Error as error:
        print("//")
        print(error)
    finally:
        if conn:
            conn.close()
            print("Connection is closed.")


def createTableMenu(conn):
    print("--- Options ---")
    print("1. Add an Employee")
    print("2. Add a Franchise")
    try:
        m_option = int(input(" >> "))
        if(m_option == 1):
            repeat = True
            while(repeat):
                insertEmployee(conn);
                optionRepeat = input("Add another employee? (Y/N): ")
                if(optionRepeat == "N"):
                    repeat = False
        elif(m_option == 2):
            repeat = True
            while(repeat):
                addFranchise(conn);
                optionRepeat = input("Add another employee? (Y/N): ")
                if(optionRepeat == "N"):
                    repeat = False

        else:
            print("--------")
    except ValueError as e:
        print(e)


def main():
    database = "MovingCompany.db"

    create_franchise_table = """CREATE TABLE IF NOT EXISTS Franchise (
                                       FID               integer     PRIMARY KEY,
                                       StreetAddress     text        NOT NULL,
                                       City              text        NOT NULL,
                                       State             text        NOT NULL,
                                       ZipCode           integer     NOT NULL,
                                       OwnerFname        text        NOT NULL,
                                       OwnerLname        text        NOT NULL
                                );"""

    create_employee_table = """CREATE TABLE IF NOT EXISTS Employee (
                                   EmpID     integer     PRIMARY KEY,
                                   Fname     text        NOT NULL,
                                   Lname     text        NOT NULL,
                                   Position  text        NOT NULL,
                                   FID       integer     NOT NULL,
                                   FOREIGN KEY (FID) REFERENCES Franchise (FID)
                            );"""

    conn = create_connection(database)

    if conn is not None:
        createTable(conn, create_franchise_table)
        createTable(conn, create_employee_table);
        createTableMenu(conn)
        conn = create_connection(database)
        c = conn.cursor();
        print("Employee Table")
        check = c.execute("SELECT * FROM Employee").fetchall()
        print(check)
        print("---------------------------------------------")
        print("Franchise Table")
        check = c.execute("SELECT * FROM Franchise").fetchall()
        print(check);
        print("---------------------------------------------")
    else:
        print("ERROR: Could not establish database connection.")

if __name__ == '__main__':
    main()

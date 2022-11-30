import sqlite3

#####################################################################################################
#                                   TWITTER ACCOUNT TABLE
#  HANDLE    NAME  
#  ------    ----  
#####################################################################################################
#                                       FOLLOWER TABLE
#  HANDLE    NAME  
#  ------    ----
#####################################################################################################


class DB:
    def create(dbname: str):
        connection = sqlite3.connect(dbname) #database name must end in .db
        c = connection.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS ACCOUNT 
        ( 
            HANDLE TEXT NOT NULL PRIMARY KEY,
            NAME TEXT NOT NULL
        ); """)

        c.execute("""CREATE TABLE IF NOT EXISTS FOLLOWER (
            HANDLE TEXT NOT NULL,
            NAME TEXT NOT NULL,
            FOREIGN KEY(ACCOUNT_HANDLE) REFERENCE ACCOUNT(HANDLE)
        ); """)

        connection.commit()
        connection.close()

    def add_account(dbname: ):

    
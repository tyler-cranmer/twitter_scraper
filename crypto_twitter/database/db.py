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
            ID TEXT NOT NULL PRIMARY KEY,
            HANDLE TEXT NOT NULL,
            TWITTERID TEXT NOT NULL
        ); """)

        c.execute("""CREATE TABLE IF NOT EXISTS FOLLOWER (
            HANDLE TEXT NOT NULL,
            TWITTERID TEXT NOT NULL,
            FOREIGN KEY(ACCOUNT_HANDLE) REFERENCE ACCOUNT(ID)
        ); """)

        connection.commit()
        connection.close()

    def add_account(dbname, handle, twitterid):
        connection = sqlite3.connect(dbname)
        c = connection.cursor()

# NEED TO ADD ACCOUNT AND FOLLOWERS TO DATABASE

        # c.execute("INSERT INTO FOLLOWER VALUES (:HANDLE, :TWITTERID);",
        #     {
        #         'HANDLE': handle,
        #         'TWITTERID': twitterid
        #     }
        # )

        # connection.commit()
        # connection.close()
    
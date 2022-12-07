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
        c.execute("""CREATE TABLE IF NOT EXISTS USERS
        ( 
            ID INTEGER PRIMARY KEY,
            HANDLE TEXT,
        ); """)

        c.execute("""CREATE TABLE IF NOT EXISTS FOLLOWERS (
            USER_ID INTEGER,
            FOLLOWER_ID INTEGER,
            FOREIGN KEY(USER_ID) REFERENCES USERS(ID)
            FOREIGN KEY(FOLLOWER_ID) REFERENCES USERS(ID)
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
    
    def get_top_n_accounts(dbname, amount):
        connection = sqlite3.connect(dbname) #database name must end in .db
        c = connection.cursor()

        c.execute("SELECT USERS.HANDLE, COUNT(FOLLOWERS.FOLLOWER_ID) AS NUM_FOLLOWERS FROM USERS JOIN FOLLOWERS ON FOLLOWERS.USER_ID = USERS.ID GROUP BY USERS.HANDLE ORDER BY NUM_FOLLOWERS DESC LIMIT :AMOUNT);",

            {
                "AMOUNT": amount
            }
        )
        db_list = list(c.fetchall())
        print(db_list)
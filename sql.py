import sqlite3

users = ['Tyler', 1234123]
ty_followers = [('_garretthughes', '1370875906831626244'), ('_denze', '1437031828938838017'), 
('daylight', '1492565486386696197'), ('SquigglCat', '1243343810756739072'), 
('lexdotpage', '1583294206386221057'), ('crossbordercap', '46745297'), 
('Pool2Paulie', '1367172848255655937'), ('0xExecLayer', '1569575466251730944'), 
('magnetmoneyshow', '1593309190524739588'), ('napgener', '1336785837288251396'), 
('matthew_pines', '1330538176121884673'), ('TennesseeStack1', '1269180467280072705'),
 ('venture_punk', '1537203675117912066'), ('skylab_xyz', '1520062917286055936'), 
 ('mhonkasalo', '146345384'), ('JordanLyall', '14910027'), ('Shnoises', '1587039381650636806'),
  ('The_BigFrank', '1362139926272372739'), ('pcaversaccio', '113203570'), 
  ('karl_0x', '1534520538164502533'), ('Volhalla_', '1524791866926899202'), 
  ('HackermanAce', '147453521'), ('NickPJackman', '1133338496746156032'), 
  ('HappyRabbitCoin', '1582526561957339136'), ('PromptNFT', '1580612266679992320'), 
  ('nftiify', '1542912474210607105'), ('magnet__art', '1579474544741556231'), 
  ('TotemMacro', '1308889929162862593'), ('VictorTheClean3', '1498447446099300358'), 
  ('OilPriceHourly', '3190569833')]
peter_followers = [('pinkpowerrangers', '1412341234'), ('redranger', '918237419083')]

connection = sqlite3.connect('practice') #database name must end in .db
mycursor = connection.cursor() #cursor 
Q1 = "CREATE TABLE IF NOT EXISTS USERS (ID INTEGER PRIMARY KEY, HANDLE CHAR(50), TWITTERID INT); "
Q2 = "CREATE TABLE IF NOT EXISTS FOLLOWERS (USERID INT, HANDLE VARCHAR(50), TWITTERID INTEGER, FOREIGN KEY(USERID) REFERENCES USERS(ID), FOREIGN KEY(TWITTERID) REFERENCES USERS(ID));"

Q3 = "INSERT INTO USERS VALUES (:HANDLE,:TWITTERID);"
Q4 = "INSERT INTO FOLLOWERS VALUES (:USERID, :HANDLE, :TWITTERID);"

# mycursor.execute(Q1)
# mycursor.execute(Q2)
sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""

# mycursor.execute(sql_query)
# print(mycursor.fetchall())


mycursor.execute("INSERT INTO USERS (HANDLE, TWITTERID) VALUES(?,?);", (users[0], users[1]))
last_id = mycursor.lastrowid
for i, followers in enumerate(ty_followers):
    mycursor.execute("INSERT INTO FOLLOWERS VALUES (:USERID, :HANDLE, :TWITTERID);", {'USERID': last_id, 'HANDLE': followers[0], 'TWITTERID': int(followers[1])})
# connection.commit()

mycursor.execute("SELECT * FROM FOLLOWERS")
for x in mycursor:
    print(x)



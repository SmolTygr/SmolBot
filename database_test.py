import sqlite3


db_connection = sqlite3.connect('testdb.db')
db_cursor = db_connection.cursor()

db_cursor.execute(f"""
                  SELECT * 
                  FROM ServerAdmins
                  WHERE ServerAdmins.ServerID="1016382572776915093" 
                  AND ServerAdmins.UserID="325726203681964043"
                  """)

print('dong')
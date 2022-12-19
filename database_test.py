import sqlite3


db_connection = sqlite3.connect('testdb.db')
db_cursor = db_connection.cursor()

db_cursor.execute(f"""
                  SELECT 
                    SAD.UserID
                  FROM ServerAdmins AS SAD
                  WHERE SAD.ServerID="1016382572776915094" 
                  """)

db_cursor.exectue(f"""
                        SELECT *
                        FROM ServerAdmins AS SAD
                        WHERE
                            SAD.ServerID="1016382572776915094"
                            AND 
                            SAD.UserID="325726203681964043"
                        """)

result = [row[0] for row in db_cursor.fetchall()]

print(result)
import mysql.connector

DB_NAME = 'streamcontrol'

def create_scoreboard(cursor):
    cursor.execute(
    "CREATE TABLE scoreboard (playerLeft char(50), playerRight char(50), scoreLeft int(1), scoreRight int(1))"
    )
    
cnx = mysql.connector.connect(user='root', password = '6549pardall', database = 'streamcontrol')
cursor = cnx.cursor()
name = 'scoreboard'
print("Creating table: " + name)
create_scoreboard(cursor)
    
